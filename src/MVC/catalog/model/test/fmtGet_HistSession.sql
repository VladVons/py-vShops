-- fmtGet_HistSession.sql
-- in: aLimit, aOffset, aHaving, aHost

with wt1 as (
    select
        hs.id,
        count(hs.id)
    from
        hist_page_view hpv
    left join
        hist_session hs on
        (hs.id = hpv.session_id)
    where
        (hs.host like '%{{aHost}}') and
        (hpv.url ~'route=|/category/|/product/|/about_us|/contacts') and
        (hs.browser not like '%bot%') and
        ((hs.uagent not like '%bot%') or (hs.uagent is null)) and
        (hs.ip  !~'127.0.0.1|5.58.222.201|5.58.78.170')
    group by
        hs.id
    having
        count(hs.id) >= {{aHaving}}
)
select
    count(*) over() as total,
    --wt1.count,
    hpv.create_date,
    hpv.url as url,
    hs.id,
    hs.ip,
    hs.browser,
    hs.os,
    hs.location
from
    hist_page_view hpv
left join
    hist_session hs on
    (hs.id = hpv.session_id)
join
    wt1 on
    (wt1.id = hpv.session_id)
where
    (hs.host like '%{{aHost}}')
--    (hpv.url like '%?route=%')
order by
    hs.id desc,
    hpv.create_date
limit
    {{aLimit}}
offset
    {{aOffset}}
