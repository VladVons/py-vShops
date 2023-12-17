-- in: aLangId, aTenantId, aProductId
select
    rp.id,
    rp.idt,
    rpl.title,
    rpl.descr,
    rpl.features,
    rpl.meta_key,
    rpcl.title as category,
    (
        select rpi.image
        from ref_product_image rpi
        where (rpi.product_id = rp.id and rpi.enabled)
        order by rpi.sort_order, rpi.image
        limit 1
    ) as image
from
    ref_product rp
left join
    ref_product_lang rpl on
    (rp.id = rpl.product_id) and (rpl.lang_id = {{aLangId}})
left join
    ref_product_to_category rptc on
    (rp.id = rptc.product_id)
left join
    ref_product_category_lang rpcl on
    (rptc.category_id = rpcl.category_id) and (rpl.lang_id = {{aLangId}})
where
    (rp.id = {{aProductId}}) and
    (rp.tenant_id = {{aTenantId}})
