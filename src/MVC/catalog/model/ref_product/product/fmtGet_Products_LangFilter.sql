select
    count(*) over() as total,
    rp.id,
    --rp.idt,
    rp.tenant_id,
    --max(rt.title),
    max(rpl.title) as title,
    min(rpp.price) as price,
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
    (rp.id = rpl.product_id) and (rpl.lang_id = {aLangId})
left join
    ref_product_barcode rpb on
    (rp.id = rpb.product_id)
left join
    ref_product_to_category rptc on
    (rp.id = rptc.product_id)
left join
    ref_product_category_lang rpcl on
    (rptc.category_id = rpcl.category_id) and (rpl.lang_id = {aLangId})
left join
    ref_price rp2 on
    (rp.tenant_id = rp2.tenant_id)
    -- and (rp2.idt in (1, 2))
left join
    ref_product_price rpp on
    (rp.id = rpp.product_id) and (rpp.qty = 1) and (rpp.price_id = rp2.id) 
--left join
--    ref_tenant rt on
--    (rp.tenant_id = rt.id) 
where
    (rpl.title ilike all (values {FilterRe})) or
    (rpcl.title ilike all (values {FilterRe})) or
    (rp.idt::varchar = '{aFilter}' ) or
    (rpb.code = '{aFilter}')
group by
    rp.id
limit
    {aLimit}
offset
    {aOffset}
