import datetime
import pandas as pd

from clock.config import connect, OUTFILE_PATH
from clock import clock_models


class ImportFile:
    def __init__(self, engine, session):
        self.engine = engine
        self.session = session

    def execute(self):
        self.read_file()
        self.insert_to_staging_table()
        self.check_row_counts()

    def read_file(self):
        """
        Read the file in as a dataframe. No attempt made to split into chunks because, presumably,
        this file will always fit into memory. If this is not the case, all that is required is
        splitting the file into chunks when we read, which in Python turns it into a generator.
        We can then truncate the staging table on each execution and then append each of the
        chunks to it.

        :return: None
        """
        print(f"...reading {OUTFILE_PATH} into dataframe. {datetime.datetime.utcnow()}")
        self.df = pd.read_csv(OUTFILE_PATH, header=None)

    def insert_to_staging_table(self):
        """
        Drop the staging table and then insert the new data into the staging table.

        :return:
        """
        print(f"...truncating clock_staging. {datetime.datetime.utcnow()}")
        self.session.execute("DROP TABLE IF EXISTS clock_staging;")
        self.session.commit()

        print(f"...inserting into clock_staging. {datetime.datetime.utcnow()}")
        self.df.columns = ["employee_id", "clock_time"]
        self.df.to_sql("clock_staging", con=self.engine)
        self.session.commit()
        print(f"...done! {datetime.datetime.utcnow()}")

    def check_row_counts(self):
        """
        Perform a quick sanity check to see if the imported file has the same number of rows as
        the staging table.

        :return: None
        """

        df_len = len(self.df)
        sql = "select count(*) from clock_staging;"
        result = self.session.execute(sql).fetchone()[0]
        if df_len != result:
            raise ValueError(
                "Count of Staging Table (clock_staging) does not match the CSV file!"
            )


def main():
    print("Importing Clock Data...")
    engine, session = connect()
    clock_models.create_models(engine=engine, session=session)

    i = ImportFile(engine=engine, session=session)
    i.execute()
