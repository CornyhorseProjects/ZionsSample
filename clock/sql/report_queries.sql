--1. Aggregate the total, annual floor time.
-- This simply sums the number of seconds per person for the whole year.  Year is implied
-- because the data only exists for a year. If we had additional yearly data, we'd have to group
-- by the year too.
drop table if exists total_annual_floor_time;
create table total_annual_floor_time as
select employee_id, sum(total_floor_time_seconds) as yearly_floor_time
    from employee_daily_report
    group by employee_id;

--2. Retrieve the employees that had the most and least amount of time for the year.
drop table if exists best_worst_25;
create table best_worst_25 as
with t1 as (
    select employee_id, yearly_floor_time
    from total_annual_floor_time
    group by employee_id
), ranked as (
    select employee_id
         , yearly_floor_time
         , row_number() over (order by yearly_floor_time desc) as rank_best
         , row_number() over (order by yearly_floor_time) as rank_worst
    from t1
    order by yearly_floor_time desc
)
select employee_id
     , yearly_floor_time as yearly_floor_time_seconds
     , yearly_floor_time / 60 / 60  as yearly_floor_time_hours
     , rank_best
     , rank_worst
from ranked
where rank_best <= 25
or rank_worst <= 25;

--3. Create a table that counts the number of total days worked, defined by anyone who had a
-- record on anyday, even if they only worked for 3 minutes (which is the lowest they could
-- theoretically work based on the way I randomly generated data).
drop table if exists attendance;
create table attendance as
    select employee_id
         , count(report_date) as total_days
    from employee_daily_report
    group by employee_id;

--4. Rank the attendance by highest and lowest number of days attended:
with ranked as (
    select employee_id
         , total_days
         , row_number() over (order by total_days desc ) as best_attendance
         , row_number() over (order by total_days )      as worst_attendance
    from attendance
    order by best_attendance
)
select employee_id
     , total_days
     , best_attendance
     , worst_attendance
from ranked
where best_attendance <= 25
or worst_attendance <= 25;

--5. Add week/month to the report:
drop table if exists weekly_monthly_totals;
create table weekly_monthly_totals as
select employee_id
     , report_date
     , strftime('%W', report_date) as week_num
     , strftime('%m', report_date) as month_num
     , start_time
     , end_time
     , total_floor_time_seconds
from employee_daily_report;

--6. Aggregate the floor time to the month level of granularity:
drop table if exists monthly_aggregate;
create table monthly_aggregate as
select month_num,
       avg(total_floor_time_seconds) as average_floor_time_seconds,
       sum(total_floor_time_seconds) as total_floor_time_seconds,
       min(total_floor_time_seconds) as min_floor_time_seconds,
       max(total_floor_time_seconds) as max_floor_time_seconds
from weekly_monthly_totals
group by month_num;

--7. Aggregate the floor time to the week level of granularity:L
drop table if exists weekly_aggregate;
create table weekly_aggregate as
select week_num,
       avg(total_floor_time_seconds) as average_floor_time_seconds,
       sum(total_floor_time_seconds) as total_floor_time_seconds,
       min(total_floor_time_seconds) as min_floor_time_seconds,
       max(total_floor_time_seconds) as max_floor_time_seconds
from weekly_monthly_totals
group by week_num;