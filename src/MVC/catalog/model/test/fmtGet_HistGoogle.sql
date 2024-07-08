--  fmtGet_HistGoogle.sql
-- in: aLimit, aOffset, aHost

with 
wt1 as (
    select 
        count(*),
        hpv.url
    from 
        hist_page_view hpv 
    join 
        hist_session hs on
        (hs.id = hpv.session_id)
    where 
        (hs.host = '{{aHost}}') and
        (hs.uagent like '%google%') and
        (hs.create_date >= '2024-06-01')
    group by
        url
)
select
    (count(*) over()) as total,
    round((count(rp.id) over()) * 100.0 / (count(*) over()), 1) as ok_pct,
    round(24 * 60.0 / count(*) over(), 1) as step_minutes,
    date_trunc('second', hpv.create_date) as create_date,
    hpv.url,
    wt1.count,
    rpl.title, 
    hs.id,
    hs.ip
from
    hist_page_view hpv
left join
    hist_session hs on
    (hs.id = hpv.session_id)
left join
    ref_seo_url rsu on
    (rsu.keyword = split_part(hpv.url, '/', -1)) and (rsu.attr = 'product_id')
left join
    ref_product rp on
    (rp.enabled) and
    (rp.id = (regexp_match(hpv.url, 'product_id=([0-9]+)'))[1]::int) or (rp.id = rsu.val::int)
left join
    ref_product_lang rpl on
    (rpl.product_id = rp.id) and (rpl.lang_id = 1)
left join 
    wt1 on
    (wt1.url = hpv.url)
where
    (hs.uagent like '%google%')
    and (hpv.create_date >= now() - interval '24 hours')
order by
    hpv.create_date desc
limit
    {{aLimit}}
offset
    {{aOffset}}
