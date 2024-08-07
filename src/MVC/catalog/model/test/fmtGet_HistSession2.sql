-- fmtGet_HistSession2.sql
-- in: aLimit, aOffset, aHaving, aHost

select
    count(*) over() as total,
    hpv.create_date,
    hpv.create_date::date::varchar as create_day,
    hpv.url,
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
where
    (hs.host like '%{{aHost}}') and
    (hpv.url ~'route=|/category/|/product/|/about_us|/contacts|/price_list') and
    (((hs.uagent not ilike '%bot%') and (hs.uagent not ilike '%facebook%')) or (hs.uagent is null)) and
    (hs.location ilike '%ukraine%') and
    (hs.ip  !~'127.0.0.1|5.58.222.201|5.58.78.170')
order by
    hpv.create_date desc
limit
    {{aLimit}}
offset
    {{aOffset}}
