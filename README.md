#Zions Samples
There are two samples in this repository:

* Parenthesis Parser
* Time Card Log In / Log Out

There are a few package requirements for each of these. They can be installed by invoking pip:

```
pip install -r /path/to/requirements.txt
```

## Parenthesis Parser
The parenthesis parser's prompt is:

    The parenthesis parsingInput: A string of open and closed parenthesis.
    Output: True or False based on if the string is a valid expression.
    Example:
        (()) returns True
        )()( returns False
        ()() returns True
        ((()) returns False
    Describe the algorithm or pseudo code to solve this challenge.


To invoke this sample, change the directory to wherever you cloned this repository to, so that 
the relative imports work correctly. Then, invoke Python and call the *parenthesis_parser_main.
py* file:

```
/path/to/python ./parenthesis_parser_main.py
```

or on Windows: 

```
c:\path\to\python.exe parenthesis_parser_main.py
```

### Method
I created one function that sanitizes the input to only contain parenthesis first.  This is not 
strictly required by the instructions, but I like to leave code that is well documented as well 
as self-evident code.  In this case, this function makes it obvious that no attempt was made to 
handle other types of brackets or handle strings of characters other than open/closed 
parenthesis.  

After this, the script is broken into two parts. While this can be handled by a single 
algorithm, I tend to prefer checking for very obvious things first.  For such a simple example 
this is not necessary but as with many projects, often simple examples end up being more 
complex.  Therefore, I've added three checks that will immediately reject a string.  If this 
were to be compiled in something such as Cython, this would typically result in a much faster 
execution time, if that ever were to be important.  It also means that for more extreme edge 
cases, that the algorithm will end up being more resilient because it rejects anything that is 
obviously wrong before sending the string along to the algorithm.  These rejection criteria 
eliminate strings if they:

* have an odd number of characters, which cannot be balanced
* have a different number of opening characters and closing characters, which also cannot be 
  balanced
* begin with a closing or end with an opening 

The algorithm itself is a simple stack, which in this case is represented by a list.  For each 
open parenthesis, a parenthesis is added to the list.  When we encounter a closed parenthesis, 
we pop it from the stack. In Python, this is LIFO (last in, first out) because Python's list.pop() 
defaults to -1. The negative first element is always the last element in a list. It continues 
in this fashion until it exhausts every element in the string.  If we have "popped" every 
element from the stack, then the parenthesis are properly balanced.  

Note that because of the way that I pre-remove obviously incorrect strings first, we circumvent 
an edge case such as "()))" where we would attempt to remove something from the stack that 
isn't there.  In this case we'd add the "(" to the stack and then remove it when it encoutners 
the next ")".  On the 3rd character it would attempt to remove another "(" that wasn't there. 
Typically, this would give us an IndexError, indicating that the index at -1 doesn't exist.  
However, because we have eliminated all strings that have different numbers of opening and 
closing brackets, we can never experience this edge case at this point, so a try/catch is not 
included.

Similarly, if we were to include a string such as "()())", it would fail for the same reason as 
the last example and also because it is an odd number.  So it is not possible to reach this 
code with a string that would result in an IndexError when assessing the stack.  Really, the 
only case that this algorithm is left to check for is something like "())(()", which has an 
even number of characters, the same number of opening and closing, and an opening 
bracket/closing bracket as the first/last characters.


## Time Card Log In / Log Out
The prompt for this is:

```Time Card Log In / Log Out

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
```
To invoke this sample, change the directory to wherever you cloned this repository to, so that 
the relative imports work correctly. Then, invoke Python and call the *parenthesis_parser_main.
py* file:

```
/path/to/python ./time_clock.py
```

or on Windows: 

```
c:\path\to\python.exe time_clock.py
```

Note that the database and .csv file that I generated are too large for a repository. Therefore,
in order to generate your own, you can uncomment line 33 of time_clock.py. However, note that 
any of the "findings" that I came up with in the report are likely to be different due to the 
nature of the random number generator in Python.

### Method
There are three parts to this script. While the prompt only asks us to discuss the ETL process, 
I went ahead and actually generated random data. I prefer working with real data when possible 
and generating such data on such a simple architecture doesn't take much time and can clarify 
any issues that might arise.

#### Fake Clock Data
There are two classes that we focus on. The first class, FakeClockData, is used to keep track 
of the generation process as a whole, and controls how many employees have clock-ins as well as 
how many clock-ins an employee has. We first generate the number of employees, between 100-500. 
Next, we loop through these using an enumeration of the range.  In the second, inner loop,
we loop through each date in the year of 2019. Finally, for each date for each employee, the 
final inner loop, we  randomly determine if the employee will clock in zero times, or 1-3 times.
We specify the "cluster" time here, so we can get up to 3 clock ins per day at morning, noon, 
and evening.  The length of each clock-in is limited so that we end up with a situation that is 
impossible for someone to stay past midnight.

The ClockIn class actually handles generating the data.  We pick a random hour and minute within 
+/- 2 hours of the "cluster" time. Then, we get a random interval that is from 1 minute to 3 
hours 59 minutes of that time and then make a "clock out".  Appending both of these values to a 
list, we can recreate the format that this time clock would be in, where no indication is given 
if someone is clocking in or clocking out.    We output to a .csv file because that is a common 
format for this type of thing to be in.  While the data itself is guaranteed to be a little 
cleaner than actual real-world data in this case, it also isn't made easier in any meaningful 
way given that we do all of the transformations in SQL, where there is no guarantee of order 
anyway.

### Import Clock Data
Importing from CSV is very simple in cases where the file fits in to memory.  Given that this 
hypothetical clock has data pulled frequently and there are presumably fewer than hundreds of 
millions of people on the floor daily, it is unlikely that the size of this would ever become 
an issue with this method. However, if for some reason it were, there are myriad ways of 
handling this, including simply chunking the reading of the file in Pandas, which can return a 
generator of lines the size of the specified chunk.  It would take an enormous amount of 
clock-ins/-outs for this to become an issue.

I elected to call this a staging table even though we're using SQLite, which doesn't have the 
concept of schema. Typically, I like to provide a logical separation from my staging areas. I 
also typically check the lines of a file, but since I'm running this on a Windows machine, I 
don't have access to the "wc -l" command I typically would invoke from Bash.  I therefore chose 
to just count the dataframe rows and compare it to the "staging" table rows.  The chance of 
this being bugged is pretty low, but CSV from legacy systems can be unpredictable at times; 
therefore, if this were a real-world system I would be more rigorous with my checking of the 
counts. I would also put more testing on the staging table to verify real-world issues that 
would arise, but were assumed to never happen because of the prompt, such as having an odd 
number of clock ins / outs for a person on a given day, etc.

### Transform Clock Data
The transformation step is quite simple now that the data is in the database.  For the purposes 
of this exercise, there are two destination tables:

* employees
* employee_daily_report

There are several intermediate tables that are built and used along the way. I copied some 
boilerplate code that I use to connect to databases from other project as well as built one 
convenience function that I used to split a SQL file into a list of strings because SQLite only 
allows one query at a time to be executed, in contrast with more robust RDBMS solutions like 
PostgreSQL.    

#### Employees
To insert employees, the *insert_employees.sql* script is executed.  This simply takes the 
employee_id from the table and makes sure they exist in the employee table.  We do a left join 
on the table on employee_id where the join is null, which gives us only employee_id that 
haven't yet been inserted.  If we were to run this query again, it would not result in an error 
because the insert would only be for new values. If no new values exist, it just does an empty 
insert.

In the Python class, I loop through these employees and randomly assign them first/last names. 
Obviously, in a real-world scenario, these names would come from somewhere else but I always 
like to put names on employees if I can and it doesn't take much time.  


#### Clock Ins
To insert clock times, we execute *include_clock_times.sql*.  This one is more involved than 
Employees. First, we get just the date for any given row, with the output being add_clock_date 
temp table.  This table is pulled and we partition by the employee_id and the date. This gives 
us up to 6 rows per person per day, ordered by clock_time.  This way, we have the ordering per 
employee per date.  Even numbers must be clock-ins and odd numbers must be clock-outs due to 
the stipulation that people can never leave the floor without clocking out.

Next, we insert the into a "clock_ins" table, which is similar to a warehouse table.  It 
contains employee_id, report_date, clock_in_number, and clock_time.  The primary key is 
employee_id, report_date, and clock_in_number. This verifies that for a given employee/date 
that they only ever have one clock in / out for a given order.  Left joining to the table on 
this primary key and specifying where it is null results in us inserting only new records.  
Note that this is not an upsert. This assumes that the clock ins will never change. If that 
were the case, we'd have to employ eitehr a slowly changing dimension to this, where we stored 
what a set of time stamps looked like at a given point in time OR by updating the table with 
more recent data, losing the old - presumably incorrect - data in the process.

Next, we apply the in/out rules. As noted, by definition cloks 1,3, and 5 must be clock-ins and 
clocks 2,4, and 6 must be clock outs.  We convert this to an "epoch", the number of seconds 
since 1970. Then, we subtract these to give us the delta in seconds in *add_floor_time_seconds* 
temp table.

To get the start/end times for a particular date, we aggregate the min/max clock_time per 
employee per report date and store it in temp table start_end_times.  

Finally, we join everything together by getting the distinct days that exist and left joining 
the aggregate_floor_time and the start_end_times from above, giving us the start/end time per 
day per employee and the total_floor_time per day per employee in the same table.  This is then 
placed in the employee_daily_report. As with above, this assumes that these data will never 
change once they have been inserted.  An upsert or slowly changing dimension would be slightly 
more difficult though could meet that requirement if it ever needed to be updatable.

Note that this format is slightly different than the one stipulated in the prompt. This is 
because the prompt is likely talking about a single day, rather than a years worth of data.  In 
a real-world application, it would make sense to have the day that an event pertains to in this 
table, so I included it. If, for some reason, this was unacceptable, creating a view that 
removed this column or generating a single table / report that was on a per-day basis would be 
trivial.

### Reporting
While it was not asked, I typically include some basic reporting the first time that I pull 
data in.  While this is a bit of a contrived example with randomly generated data,

