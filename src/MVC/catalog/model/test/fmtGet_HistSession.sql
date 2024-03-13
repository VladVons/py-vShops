-- fmtGet_HistSession.sql
-- in: aLimit, aOffset, aHaving

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
        (url like '%?route=%') and
        (browser not like '%bot%') and
        (ip not like '217.196.161.%') and
        (ip not like '127.0.0.1')
    group by
        hs.id
    having
        count(hs.id) >= {{aHaving}}
),
wt2 as (
    select
        count(*) over() as total,
        --wt1.count,
        hpv.create_date,
        hpv.url as url,
        --'https://used.1x1.com.ua' || hpv.url as url,
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
        (url like '%?route=%')
    order by
        hs.id desc,
        hpv.create_date
    limit
        {{aLimit}}
    offset
        {{aOffset}}
)
select *
from wt2
