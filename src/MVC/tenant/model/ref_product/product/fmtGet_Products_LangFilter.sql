-- in: aLangId, FilterRe, aOrder, aLimit, aOffset
select
    count(*) over() as total,
    rp.id,
    rp.idt,
    rp.product0_id,
    rptc.category_id,
    rpl.title,
    rpcl.title as category_title,
    (
        select rpp.price
        from ref_product_price rpp
        left join ref_product_price_date rppd on 
            (rpp.id  = rppd.product_price_id)
        left join ref_price on 
            (rpp.price_id = ref_price.id)
        where
            (rpp.enabled) and 
            (ref_price.price_en = 'sale') and
            ((rpp.product_id = rp.id) and (rppd.id is null)) or
            ((rpp.product_id = rp.id) and rppd.enabled and (now() between rppd.begin_date and rppd.end_date))
        order by rpp.price
        limit 1
    ) as price,
    (
        select rpi.image
        from ref_product_image rpi
        where (rpi.product_id = rp.id and rpi.enabled)
        order by rpi.sort_order
        limit 1
    ) as image
from
    ref_product rp
left join
    ref_product_lang rpl on
    (rp.id = rpl.product_id) and (rpl.lang_id = {{aLangId}})
left join
    ref_product_barcode rpb on
    (rp.id = rpb.product_id)
left join
    ref_product_to_category rptc on
    (rp.id = rptc.product_id)
left join
    ref_product_category_lang rpcl on
    (rptc.category_id = rpcl.category_id) and (rpl.lang_id = {{aLangId}})
where
    (rp.tenant_id = {{aTenantId}}) and
    (rpl.title ilike all (values {{FilterRe}})) or
    (rpcl.title ilike all (values {{FilterRe}})) or
    (rp.idt::varchar = '{{aFilter}}' ) or
    (rpb.code = '{{aFilter}}')
order by
    {{aOrder}}
limit
    {{aLimit}}
offset
    {{aOffset}}
