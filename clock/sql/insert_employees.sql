--1. Create a distinct table of the employee_ids.  Note that this isn't totally necessary,
--   later we'll do a left join but I find that in cases where I'd do this, I'll often use
--   distincts at the staging layer because there's usually a lot less data and so it might save
--   a little execution time doing it this way. Additionally, making a table like this can be
--   indexed if we really need to increase performance. For this particular project it obviously
--   is extreme overkill, but since I'd typically do this, I'm making it nonetheless.
drop table if exists distinct_employees;
create temp table distinct_employees as
with t1 as (
    select distinct employee_id
    from clock_staging
    order by employee_id
)
select employee_id
from t1;

--2. Insert into the table. Note that we don't have first/last names in this example.
-- Presumably, we'd have it in some capacity in a real-world example.  We'll create new names
-- with faker in Python, so we'll just leave them blank for the moment.

--Doing a left join on the table we're inserting into means that we can run this without running
-- into an error if the ID already exists.  This is chosen over something like the Postgres
-- syntax "ON CONFLICT DO NOTHING" because this won't exhaust IDs.  With that sytnax, every time
-- you try to insert a row, it iterates the sequence, so you end up with sometimes enormous gaps
-- in the IDs. In and of itself this isn't a huge deal, but we can easily circumvent it with
-- this method.  If this is not performant, we can consider adding indexes depending on what the
-- bottleneck is OR using a syntax like that in the event that we don't forsee running out of
-- IDs... bigints have billions of rows of availability and UUIDs can substitute in cases where
-- this is a possibility.
INSERT INTO employee(employee_id)
select e.employee_id
from distinct_employees de
left join employee e on de.employee_id = e.employee_id
where e.employee_id is null;


--Clean Up:
drop table if exists distinct_employees;