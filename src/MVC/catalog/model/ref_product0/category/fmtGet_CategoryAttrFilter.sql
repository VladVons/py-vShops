-- fmtGet_CategoryAttrFilter.sql
-- aLangId, aCategoryId, CondAttrAndVal_ORs, NumberOf_ORs,

with
wt1 as (
    {% include './fmtGet_CategoryAttrFilterProduct.sql' %}
),
wt2 as (
    select
        rpa.attr_id,
        rpa.val,
        count(*)
    from
        ref_product_attr rpa
    join
        wt1 on
        (wt1.product_id = rpa.product_id)
    group by
        rpa.attr_id,
        rpa.val
)
select
    wt2.attr_id,
    wt2.val,
    wt2.count,
    ra.alias,
    ral.title
from
    wt2
join
    ref_attr_lang ral on
    (ral.attr_id = wt2.attr_id) and (ral.lang_id = {{aLangId}})
join
    ref_attr ra on
    (ra.id = wt2.attr_id)
order by
    title,
    val
