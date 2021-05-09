--First, we'll add just the clock_date to the table. This lets us add a row number and partition
-- by the date of the clock in.
drop table if exists add_clock_date;
create temp table add_clock_date as
    select employee_id
         , date(clock_time) as clock_date
         , clock_time
    from clock_staging;

--Next, we'll add a row number that is partitioned by the employee_id and the clock_date.  In
-- this case, if there are 6 clocks ins for employee_id 0 on 2019-01-01, then there will be 6
-- rows, ordered sequentially.
drop table if exists add_clock_date_row_number;
create temp  table add_clock_date_row_number as
select employee_id
     , clock_date
     , clock_time
     , row_number() over (partition by employee_id, clock_date order by employee_id, clock_time)
      as employee_clock_date_order
from add_clock_date
order by employee_id, clock_date, clock_time;

--SQLite doesn't allow us to alter a table to add a primary key, so we just create one that has
-- the primary key enforcement on it.  This way, we verify that no employee_id is inserted that
-- doesn't exist in the employee table. Additionally, we make sure we eliminate any duplicates
-- etc. by primary key enforcement.
INSERT INTO clock_ins(employee_id, report_date, clock_in_number, clock_time)
SELECT t1.employee_id
     , t1.clock_date as report_date
     , t1.employee_clock_date_order as clock_in_number
     , t1.clock_time
from add_clock_date_row_number t1
left join clock_ins t2 on t1.employee_id = t2.employee_id
                      and t1.clock_date = t2.report_date
                      and t1.employee_clock_date_order = t2.clock_in_number
where t2.employee_id is null
  and t2.report_date is null
  and t2.clock_in_number is null;


--Clock ins must be odd, clock_outs must be even.  In this smal lsample set, the maximum we have
-- are 6 total clock events in a day so I just hard coded this.
drop table if exists join_ins_to_outs;
create temp table join_ins_to_outs as
with ins as (
    select employee_id, report_date, clock_in_number, clock_time
    from clock_ins
    where clock_in_number in (1, 3, 5)
), outs as (
    select employee_id, report_date, clock_in_number, clock_time
    from clock_ins
    where clock_in_number in (2,4,6)
)
select i.employee_id,
       i.report_date,
       i.clock_in_number,
       o.clock_in_number as clock_out_number,
       i.clock_time as clock_in_time,
       o.clock_time as clock_out_time,
       strftime('%s', i.clock_time) clock_in_epoch,
       strftime('%s', o.clock_time) clock_out_epoch
from ins i
--Joins ins to the outs, which are by definition the next sequential event:
inner join outs o on i.employee_id = o.employee_id
                 and i.report_date = o.report_date
                 and i.clock_in_number + 1= o.clock_in_number;

--Next, we'll calculate the difference, in seconds, of the in vs the out:
drop table if exists add_floor_time_seconds;
create temp table add_floor_time_seconds as
select employee_id
     , report_date
     , clock_in_number
     , clock_out_number
     , clock_in_time
     , clock_out_time
     , clock_in_epoch
     , clock_out_epoch
     , clock_out_epoch - clock_in_epoch as floor_time_seconds
from join_ins_to_outs;

--Finally for this step, we'll aggregate the total floor time:
drop table if exists aggregate_floor_time;
create temp table aggregate_floor_time as
    select employee_id
         , report_date
         , sum(floor_time_seconds) as total_floor_time
    from add_floor_time_seconds
group by employee_id, report_date;

--To get the start/end time of an employee, we can do a simple aggregation:
drop table if exists start_end_times;
create temp table start_end_times as
select employee_id
     , report_date
     , min(clock_time) as start_time
     , max(clock_time) as end_time
from clock_ins
group by employee_id, report_date
order by employee_id, report_date;

--Now, we'll just get the employee/days and join them to the two reports from above. Note that
-- left joins were chosen over inner joins. Technically, they should produce identical output.
-- If I were doing this in a more robust fashion, I would include some error handling here to
-- make sure that the left joins didn't produce any NULL values, because if we do, there woudl
-- be a problem.
drop table if exists join_all;
create temp table join_all as
with distinct_days as (
    select distinct employee_id, report_date
    from clock_ins
)
select t1.employee_id
     , t1.report_date
     , start_time
     , end_time
     , total_floor_time
from distinct_days t1
left join aggregate_floor_time t2 on t1.employee_id = t2.employee_id
                                   and t1.report_date = t2.report_date
left join start_end_times t3 on t3.employee_id = t1.employee_id
                            and t3.report_date = t1.report_date;

INSERT INTO employee_daily_report(employee_id, report_date, start_time, end_time, total_floor_time_seconds)
SELECT t1.employee_id
     , t1.report_date
     , t1.start_time
     , t1.end_time
     , total_floor_time
from join_all t1
left join employee_daily_report t2 on t1.employee_id = t2.employee_id
                                  and t1.report_date = t2.report_date
where t2.employee_id is null
  and t2.report_date is null;



--Clean up:
drop table if exists add_clock_date;
drop table if exists add_clock_date_row_number;
drop table if exists join_ins_to_outs;
drop table if exists add_floor_time_seconds;
drop table if exists aggregate_floor_time;
drop table if exists start_end_times;