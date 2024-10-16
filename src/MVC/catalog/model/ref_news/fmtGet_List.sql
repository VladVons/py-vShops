-- fmtGet_list.sql
-- aGroupId, aLangId, aLimit, aOffset

select
    count(*) over() as total,
    rn.id,
    coalesce(rn.public_date, rn.create_date) as public_date,
    rnl.title,
    rnl.descr,
    rnl.meta_key,
    rnl.image
from
    ref_news rn
join
    ref_news_lang rnl on
    (rnl.news_id = rn.id) and (rnl.lang_id = {{aLangId}})
where
    (rn.enabled) and
    ((rn.public_date < now()) or (rn.public_date is null)) and
    (rn.group_id = {{aGroupId}}) and
    (tenant_id = 0)
order by
    public_date desc
limit
    {{aLimit}}
offset
    {{aOffset}}
