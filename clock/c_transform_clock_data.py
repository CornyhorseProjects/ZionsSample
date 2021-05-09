import datetime
from faker import Faker

from clock.config import connect
from clock import clock_models as cm
from clock.clock_models import execute_sql_file


class Transform:
    """
    The transform class is takes data that we imported from the CSV and inserts it into the
    destination tables.
    """
    def __init__(self, engine, session):
        self.engine = engine
        self.session = session

    def execute(self):
        """
        This will be the only method that an end-user would realistically call. It ties all of
        the parts of this pipe into the same method as a convenience.

        :return: None
        """
        self.import_employees()
        self.import_clock_times()
        self.run_report_queries()

    def import_employees(self):
        """
        Does an insert by invoking the insert_employees.sql file located in clock.sql.  Note that
        this can be ran without error even if it has already been executed. After we have the
        all of the employee_ids imported, we add fake names to them. If they've already been
        imported, it'll rename every person.

        :return:
        """
        print(f"...importing employees. {datetime.datetime.utcnow()}")
        execute_sql_file('insert_employees.sql', self.session)

        faker = Faker()
        for i, employee in enumerate(self.session.query(cm.Employee)):
            print(f"...adding fake name for employee: {i}")

            employee.employee_first_name = faker.first_name()
            employee.employee_last_name = faker.last_name()
            self.session.merge(employee)
            self.session.commit()


    def import_clock_times(self):
        """
        Runs the SQL query that pulls in the clock times from the staging table to the
        destination table.

        :return: None
        """
        print(f"...importing clock times. {datetime.datetime.utcnow()}")
        execute_sql_file('insert_clock_times.sql', self.session)

    def run_report_queries(self):
        """
        These reports are used to determine basic information about the habits of these employees.

        :return None
        """
        print(f"...running report queries. {datetime.datetime.utcnow()}")
        execute_sql_file('report_queries.sql', self.session)


def main():
    """
    This function is included to keep clutter out of the Python file that calls it.

    :return: None
    """
    print("Transforming data from staging area...")
    engine, session = connect()
    cm.create_models(engine=engine, session=session)

    t = Transform(engine, session)
    t.execute()