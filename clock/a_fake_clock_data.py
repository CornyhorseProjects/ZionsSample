import csv
import datetime
import os
import random
import pandas as pd

from clock.config import OUTFILE_PATH


def clean_file():
    try:
        os.unlink(OUTFILE_PATH)
    except FileNotFoundError:
        pass


class ClockIn:
    def __init__(self, employee_id, date, cluster_around):
        self.employee_id = employee_id
        self.date = date
        self.cluster_around = cluster_around
        self.clock_in_time = None
        self.clock_out_time = None
        self.lines_to_write = []

    def create_clock_in(self):

        rand_hour = random.randint(self.cluster_around - 2, self.cluster_around + 2)
        rand_minute = random.randint(0, 59)

        random_hours = random.randint(0, 3)
        random_minutes = random.randint(1, 59)
        delta = datetime.timedelta(hours=random_hours, minutes=random_minutes)

        self.clock_in_time = datetime.datetime(
            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
            hour=rand_hour,
            minute=rand_minute,
        )

        self.clock_out_time = self.clock_in_time + delta
        self.lines_to_write = [
            [self.employee_id, self.clock_in_time],
            [self.employee_id, self.clock_out_time],
        ]
        print(
            f"Generating clock in for {self.employee_id} on {self.date} around "
            f"{self.cluster_around} {self.clock_in_time} -> {self.clock_out_time}"
        )

        self.write_to_file()

    def write_to_file(self):
        with open(OUTFILE_PATH, "a") as csv_file:
            for line in self.lines_to_write:
                writer = csv.writer(csv_file, delimiter=",", quotechar="|", lineterminator='\n')
                writer.writerow(line)


class FakeClockData:
    """
    This class creates fake clock data.  Chosen as a class rather than a function purely to have
    the class attributes employees and date_list.  Putting them in the class is a little more
    explicit than what I'd do functionally.

    Generates a random list of employees and specifies the date range for those employees.

    """
    def __init__(self):
        self.employees = 0
        self.date_list = []

    def generate_random_data(self):
        """
        The primary class that you'd call as an end-user.  This simply calls all of the other
        methods together; first it generates the employee IDs, then it generates a list of dates.
        Last, it does a nested loop of these to generate clock data for each employee per date.

        :return: None
        """
        self.generate_employee_ids()
        self.generate_date_list()
        self.generate_timestamps_per_person()

    def generate_employee_ids(self):
        """
        Randomly generate the number of employees that exist.

        :return: None
        """
        self.employees = random.randint(100, 500)

    def generate_date_list(self):
        """
        Generate a list of dates between two points. Convert from the Pandas library timestamp
        datatype to the Python built-in datatype using a generator.

        :return: None
        """
        self.date_list = [
            a.to_pydatetime() for a in list(pd.date_range("2019-01-01", "2020-01-01"))
        ]

    def generate_timestamps_per_person(self):
        """
        This loops through the list of each employees and dates in the sample time period. For
        each person/date, there is a random number (including 0) clock-ins that can occur.  Up to 3,
        so that they never inadvertently stay over midnight.

        The "cluster around" gives you a +/- 2:59 hour range. If you specify 6, you can clock in
        anytime from 4:00AM to 8:59AM.

        The ClockIn class is created 3 times, each with it's own cluster time.  These are,
        as noted above, invoked specifically to avoid going over. The latest possible time is 16
        + 2 hours = 18 (6PM) :59 to start and then 3:59 after that, which is 10:58PM.

        :return: None
        """
        for employee_id in range(self.employees):
            for date in self.date_list:
                daily_clock_ins = random.randint(0, 3)

                if daily_clock_ins >= 1:
                    ci = ClockIn(employee_id=employee_id, date=date, cluster_around=6)
                    ci.create_clock_in()

                if daily_clock_ins >= 2:
                    ci = ClockIn(employee_id=employee_id, date=date, cluster_around=11)
                    ci.create_clock_in()

                if daily_clock_ins == 3:
                    ci = ClockIn(employee_id=employee_id, date=date, cluster_around=16)
                    ci.create_clock_in()


def main():
    """
    Generate fake data to file.
    :return: None
    """
    clean_file()
    fcd = FakeClockData()
    fcd.generate_random_data()
