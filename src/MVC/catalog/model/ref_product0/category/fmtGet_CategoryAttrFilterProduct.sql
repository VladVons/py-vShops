-- fmtGet_fmtGet_CategoryAttrFilterProduct.sql
-- aLangId, aCategoryId, CondAttrAndVal_ORs, NumberOf_ORs

select
    rpa.product_id
from
    ref_product_attr rpa
join
    ref_product rp on
    (rp.id = rpa.product_id)
join
    ref_tenant rt on
    (rt.id = rp.tenant_id)
join
    ref_product0_to_category rptc0 on
    (rptc0.product_id = rp.product0_id)
where
    (rp.enabled) and
    (rp.product0_id is not null) and
    (rt.enabled) and
    (rptc0.category_id = {{aCategoryId}}) and
    (rpa.lang_id = {{aLangId}}) and
    (
        {{CondAttrAndVal_ORs}}
        --(rpa.attr_id = 1 and rpa.val in ('8GB', '16GB')) or
        --(rpa.attr_id = 4 and rpa.val IN ('256GB', '500GB'))
    )
group by
    rpa.product_id
having
    count(*) = {{NumberOf_ORs}}
