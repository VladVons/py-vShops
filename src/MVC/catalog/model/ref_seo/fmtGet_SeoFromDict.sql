-- fmtGet_SeoFromDict.sql
-- in: Data(attr, val, idx), ...


with 
src as ( 
    select attr, val, idx
    from (
        values {{Data}}
    ) as t1 (attr, val, idx)
),
wt1 as ( 
    select
        rsu.attr || '=' || rsu.val as attr_val,
        rsu.keyword,
        rsu.sort_order,
        src.idx
    from
        ref_seo_url rsu
    join
        src on
        (src.attr = rsu.attr) and (src.val = rsu.val)
    order by
        src.idx,
        rsu.sort_order
),
wt2 as (
    select
        attr_val,
        keyword,
        sort_order,
        idx
    from wt1
    
    union all
    
    select 
        src.attr || '=' || src.val,
        null,
        10,
        src.idx
    from src
    left join wt1 on 
        (wt1.attr_val = (src.attr || '=' || src.val))
    where 
        wt1.attr_val is null
)
select
    idx,
    array_agg(array[keyword, attr_val] order by sort_order) as url
from 
    wt2
group by 
    idx
order by
    idx
