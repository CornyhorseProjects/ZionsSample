from sqlalchemy import create_engine, orm
import os

OUTFILE_PATH = os.path.join(os.curdir, "time_file.csv")
DB_PATH = os.path.join(os.curdir, "clock.db")
SQL_PATH = os.path.join(os.curdir, "clock/sql")


def connect():
    engine = create_engine(f'sqlite:///{DB_PATH}')
    Session = orm.sessionmaker(autoflush=False)
    Session.configure(bind=engine)
    session = Session()

    return engine, session
