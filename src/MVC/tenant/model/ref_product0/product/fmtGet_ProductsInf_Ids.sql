-- in: aLangId, aProductIds
select
    rp.id,
    rpl.title,
    rptc.category_id,
    rpcl.title as category_title,
    array (
        select image
        from ref_product0_image
        where (product_id = rp.id) and enabled
        order by sort_order
    ) as images
from
    ref_product0 rp
left join
    ref_product0_lang rpl on
    (rp.id = rpl.product_id) and (rpl.lang_id = {{aLangId}})
left join
    ref_product0_to_category rptc on
    (rp.id = rptc.product_id)
left join
    ref_product0_category_lang rpcl on
    (rptc.category_id = rpcl.category_id) and (rpl.lang_id = {{aLangId}})
where
    (rp.id in (aProductIds))
