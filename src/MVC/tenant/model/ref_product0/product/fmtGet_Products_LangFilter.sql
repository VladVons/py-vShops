-- in: aLangId, FilterRe, aOrder, aLimit, aOffset
select
    count(*) over() as total,
    rp.id,
    rptc.category_id,
    rpl.title as product_title,
    rpcl.title as category_title,
    (
        select rpi.image
        from ref_product0_image rpi
        where (rpi.product_id = rp.id and rpi.enabled)
        order by rpi.sort_order
        limit 1
     ) as image
from
    ref_product0 rp
left join
    ref_product0_lang rpl on
    (rp.id = rpl.product_id) and (rpl.lang_id = {{aLangId}})
left join
    ref_product0_barcode rpb on
    (rp.id = rpb.product_id)
left join
    ref_product0_to_category rptc on
    (rp.id = rptc.product_id)
left join
    ref_product0_category_lang rpcl on
    (rptc.category_id = rpcl.category_id) and (rpl.lang_id = {{aLangId}})
where
    (rp.enabled) and
    (
        (rpl.title ilike all (values {{FilterRe}})) or
        (rpcl.title ilike all (values {{FilterRe}})) or
        (rpb.code = '{{aFilter}}')
    )
order by
    {{aOrder}}
limit
    {{aLimit}}
offset
    {{aOffset}}
