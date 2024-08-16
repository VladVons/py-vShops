-- fmtGet_HistUniqIpPerDay.sql
-- in: aHost, aLimit, aOffset

select
    count(*) over() as total,
    count(*),
    --extract(dow from hpv.create_date::date)+1 as dow,
    TO_CHAR(hpv.create_date::date, 'Day') AS dow,
    hpv.create_date::date::varchar as create_day,
    count(distinct hs.ip) as count_ip,
    count(distinct hs.id) as count_id,
    count(distinct hs.location) as count_location,
    count(distinct hpv.url) as count_url
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
group by
    hpv.create_date::date
order by 
    create_day desc
limit
    {{aLimit}}
offset
    {{aOffset}}
