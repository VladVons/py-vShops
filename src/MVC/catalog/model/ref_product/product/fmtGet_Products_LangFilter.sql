-- in: aLangId, FilterRe, aOrder, aLimit, aOffset
select
    count(*) over() as total,
    rp.id as product_id,
    rptc.category_id,
    rp.tenant_id,
    rt.title as tenant_title,
    rpl.title as product_title,
    (
        select rpp.price::float
        from ref_product_price rpp
        where (rp.id = rpp.product_id) and (rpp.qty = 1)
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
    ref_tenant rt on
    (rp.tenant_id = rt.id)
where
    (rp.enabled) and
    (
        (rpl.title ilike all (values {FilterRe})) or
        (rpcl.title ilike all (values {FilterRe})) or
        (rp.idt::varchar = '{aFilter}' ) or
        (rpb.code = '{aFilter}')
    )
order by
    {aOrder}
limit
    {aLimit}
offset
    {aOffset}
