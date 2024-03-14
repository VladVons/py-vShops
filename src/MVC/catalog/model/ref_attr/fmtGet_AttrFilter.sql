-- fmtGet_AttrFilter.sql

select
    pcfg.category_id,
    pcfg.title,
    array_agg(array[pcf.attr_id::varchar, pcf.val, pcf.val_max]) as filter
from
    ref_product0_category_filter pcf
join
    ref_product0_category_filter_group pcfg on
    (pcfg.id = pcf.filter_group_id)
group by
    pcfg.id
order by
    pcfg.title
