-- fmtGet_AttrFilter.sql

select 
    rafg.title,
    array_agg(array[raf.category_id::varchar, raf.attr_id::varchar, raf.val, raf.val_max])
from 
    ref_attr_filter raf 
join
    ref_attr_filter_group rafg on
    (rafg.id = raf.attr_filter_group_id)
group by
    rafg.id
order by 
    rafg.title
