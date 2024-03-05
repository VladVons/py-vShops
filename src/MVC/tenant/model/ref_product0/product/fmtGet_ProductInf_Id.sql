-- fmtGet_ProductInf_Id.sql
-- in: aLangId, aId

select
    rp.id,
    rp.create_date::date,
    rpl.title,
    rpl.descr,
    rpl.features,
    rpl.meta_key,
    rptc.category_id,
    rpcl.title as category_title,
    array (
        select rpi.image
        from ref_product0_image rpi
        where (rpi.product_id = rp.id) and (rpi.enabled)
        order by rpi.sort_order, rpi.image
    ) as images,
    (
        select jsonb_object_agg(product_en, code)
        from ref_product0_barcode
        where product_id = rp.id 
    ) as barcodes
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
    (rp.id = {{aId}})
