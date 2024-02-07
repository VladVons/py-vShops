-- in: aTable, aField
select 
    field + 1 as gap_start, 
    next_nr - 1 as gap_end
from (
    select 
        {{aField}} as field, 
        lead({{aField}}) over (order by {{aField}}) as next_nr
    from {{aTable}}
) as t1
where (field + 1 != next_nr)
