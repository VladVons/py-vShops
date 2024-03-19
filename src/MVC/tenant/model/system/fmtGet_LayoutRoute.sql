-- fmtGet_LayoutRoute.sql
--in: aLimit, aOffset

select
    count(*) over() as total,
    route,
    title
from
    ref_layout rl
join
    ref_layout_lang rll on
    rll.layout_id = rl.id
where
    (rl.enabled)
order by
    rll.title
limit
    {{aLimit}}
offset
    {{aOffset}}
