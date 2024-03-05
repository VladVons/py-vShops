-- fmtGet_CategoryAttrFilter.sql
-- aLangId, aCategoryId, CondAttrAndVal_ORs, NumberOf_ORs,

with
wt1 as (
    {% include './fmtGet_CategoryAttrFilterProduct.sql' %}
)
select
    rpa.attr_id,
    rpa.val,
    max(ral.title) as title,
    count(*)
from
    ref_product_attr rpa
join
    ref_attr_lang ral on
    (ral.attr_id = rpa.attr_id) and (ral.lang_id = {{aLangId}})
join
    wt1 on
    (wt1.product_id = rpa.product_id)
group by
    rpa.attr_id,
    rpa.val
order by
    title,
    val
