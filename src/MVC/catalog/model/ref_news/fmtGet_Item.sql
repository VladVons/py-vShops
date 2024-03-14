-- fmtGet_Item.sql
-- in: aNewsId, aLangId

select
    coalesce(rn.public_date, rn.create_date)::date as public_date,
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
    (rn.id = {{aNewsId}}) and
    ((rn.public_date < now()) or (rn.public_date is null)) and
    (tenant_id = 0)
