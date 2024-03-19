-- fmtGet_LayoutRoute.sql

select
    route,
    title
from
    ref_layout rl
join
    ref_layout_lang rll on
    rll.layout_id = rl.id
where
    (rl.enabled) and
    (rl.sitemap)
order by
    rll.title
