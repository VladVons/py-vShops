-- fmtGet_CategoryDescrRnd.sql
-- in: aLangId, aCategoryId

select
    descr
from
    ref_product0_category_rnd_lang
where
    enabled and
    (lang_id = {{aLangId}}) and 
    ((category_id = {{aCategoryId}}) or (category_id is null))
order by
    category_id, 
    random()
limit 
    1
