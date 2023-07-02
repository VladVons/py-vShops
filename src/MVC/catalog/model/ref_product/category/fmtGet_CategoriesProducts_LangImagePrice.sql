-- in: aLangId, aPriceId, CategoryIds, aOrder, aLimit, aOffset
select
    rptc.category_id,
    rptc.product_id,
    rp.tenant_id,
    rpl.title,
    (
        select rpp.price
        from ref_product_price rpp
        left join ref_product_price_date rppd on (rpp.id  = rppd.product_price_id)
        where (rpp.enabled) and
            ((rpp.product_id = rp.id) and (rppd.id is null)) or
            ((rpp.product_id = rp.id) and rppd.enabled and (now() between rppd.begin_date and rppd.end_date))
        order by rpp.price
        limit 1
    ) as price,
    (
        select rpi.image
        from ref_product_image rpi
        where (rpi.product_id = rptc.product_id and rpi.enabled)
        order by rpi.sort_order
        limit 1
     ) as image
from
    ref_product_to_category rptc
left join
    ref_product rp on
    (rptc.product_id = rp.id and rp.enabled)
left join
    ref_product_lang rpl
    on (rptc.product_id = rpl.product_id and rpl.lang_id = {aLangId})
where
    (rptc.category_id in ({CategoryIds}))
order by
    {aOrder}
limit
    {aLimit}
offset
    {aOffset}
