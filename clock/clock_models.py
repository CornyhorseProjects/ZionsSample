from sqlalchemy import (
    Column,
    INTEGER,
    TEXT,
    TIMESTAMP,
    ForeignKey,
    DATE,
)
from sqlalchemy.ext.declarative import declarative_base
import datetime
import os

Base = declarative_base()

from clock.config import SQL_PATH


class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(INTEGER, primary_key=True, autoincrement=True)
    employee_first_name = Column(TEXT)
    employee_last_name = Column(TEXT)


class ClockIns(Base):
    __tablename__ = 'clock_ins'

    employee_id = Column(INTEGER, ForeignKey(Employee.employee_id), primary_key=True)
    report_date = Column(DATE, primary_key=True)
    clock_in_number = Column(INTEGER, primary_key=True)
    clock_time = Column(TIMESTAMP)


class EmployeeDailyReport(Base):
    __tablename__ = "employee_daily_report"

    employee_id = Column(INTEGER, ForeignKey(Employee.employee_id), primary_key=True)
    report_date = Column(DATE, primary_key=True)
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    total_floor_time_seconds = Column(INTEGER)


def create_models(engine, session):
    print(f"Creating Tables... {datetime.datetime.now()}")
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def read_sql_file(file_name):
    """
    Convenience function.  Not particularly modular in this sample.  Normally, I'd make it a
    little more portable but in this case I will only ever use it in this directory so it's fine
    the way it is.  Accepts the name of the file to run and then returns a list of SQL commands
    from that file.  SQLite doesn't allow multiple commands to be executed simultaneously,
    or else I'd just execute the file itself.

    :param file_name: Name of the file to import.
    :return: A list of SQL commands to be executed.
    :rtype: list
    """
    full_path = os.path.abspath(os.path.join(SQL_PATH, file_name))
    with open(full_path, 'r') as f:
        return f.read().strip().split(';')


def execute_sql_file(file_name, session):
    """
    Accepts the name of a file and a SQLAlchemy session object.  Calls the read_sql_file
    functionality, which pulls a text file from the file system, reads it, and returns a list of
    SQL comands to run. This command then iterates through them and commits at the end,
    which mimics the functionality of more robust RDBMS solutions.

    :param file_name: Name of the file to execute
    :param session:  A SQLAlchemy session object
    :return: None
    """
    sql_list = read_sql_file(file_name)
    for sql in sql_list:
        session.execute(sql)
    session.commit()

