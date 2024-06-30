-- fmtGet_Products_WithoutDescr.sql
-- in: aLangId, aTenantId, aCtegories, aLimit

select
    count(*) over() as total,
    rp.id,
    rp.cond_en,
    rpl.title,
    rpcl.title as category_title,
    (
        select array_agg(array[ral.title, rpa.val])
        from ref_product_attr rpa
        left join ref_attr ra on (ra.id = rpa.attr_id)
        left join ref_attr_lang ral on (ral.attr_id = ra.id and ral.lang_id = {aLangId})
        where (rpa.product_id = rp.id)
    ) as attr
from
    ref_product rp
left join
    ref_product_lang rpl on
    (rp.id = rpl.product_id) and (rpl.lang_id = {aLangId})
left join
    ref_product_to_category rptc on
    (rp.id = rptc.product_id)
left join
    ref_product_category_lang rpcl on
    (rptc.category_id = rpcl.category_id) and (rpl.lang_id = {aLangId})
left join
    reg_product_stock rps on
    (rp.id = rps.product_id)
where
    (rp.enabled) and
    (rp.product0_id is not null) and
    (rp.tenant_id = {aTenantId}) and
    (rps.rest > 0) and
    (rpl.descr is null) and
    (rpcl.title in ({aCategories}))
limit
    {aLimit}
