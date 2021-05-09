from clock import a_fake_clock_data, b_import_clock_data, c_transform_clock_data


"""

Time Card Log In / Log Out

When employees comes into work, they will swipe in to get on to the floor. When they leave to 
take coffee or lunch breaks, they will swipe out to leave the floor. When they come back from the 
break, they will swipe in to get back on the floor. When they go home for the day, they will 
swipe out to leave the floor.

The source file will have two columns: Employee ID and the timestamp for each time a card is swiped.

* The records in the source file are not sorted.
* Each record does not indicate if the timestamp is swipe in or swipe out.

The target file will need to have four columns:

* Employee ID
* Start Time - The first time the employee swiped in for the day.
* End Time - The last time the employee swiped out for the day.
* Total time spent on the floor. This field must negate all the breaks that were taken during the 
day.

Describe the ETL solution.

"""


if __name__ == '__main__':
    if False:
        # Run this to re-generate fake data:
        a_fake_clock_data.main()

    b_import_clock_data.main()
    c_transform_clock_data.main()