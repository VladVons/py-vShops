-- aLangId, aCategoryId
--and (rpa.attr_id = 1 and (rpa.val = '8GB' or rpa.val = '16GB'))

with wt1 as (
    select
        rpa.attr_id,
        rpa.val,
        max(ral.title) as title,
        count(*)
    from
        ref_product0_to_category rptc0
    join
        ref_product rp on
        (rptc0.product_id = rp.product0_id)
    join
        ref_product_attr rpa on
        (rpa.product_id = rp.id) and (rpa.lang_id = {{aLangId}})
    join
        ref_attr_lang ral on
        (ral.attr_id = rpa.attr_id) and (ral.lang_id = {{aLangId}})
    join
        ref_tenant rt on
        (rp.tenant_id = rt.id)
    where
         (rptc0.category_id = {{aCategoryId}}) and
         (rp.enabled) and
         (rp.product0_id is not null) and
         (rt.enabled)
    group by
        rpa.attr_id,
        rpa.val
    order by
        title,
        val
)
select
    attr_id,
    title,
    jsonb_object_agg(val, count) as attrs
from
    wt1
group by
    attr_id,
    title
order by
    title
