-- fmtGet_SeoFromDict.sql
-- in: aLangId, AttrVal(attr, val), ...

with src (attr, val) as (
    values {{AttrVal}}
)
select
    distinct(rsu.attr || '=' || rsu.val) as attr_val,
    rsu.keyword
from
    ref_seo_url rsu
join
    src on
    (src.attr = rsu.attr) and (src.val = rsu.val)
where
    (lang_id = 1)
