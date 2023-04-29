select
    rptc.category_id,
    rptc.product_id,
    rp.tenant_id,
    rpl.title,
    rpp.price,
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
left join
    ref_product_price rpp 
    on (rptc.product_id = rpp.product_id and rpp.price_id = {aPriceId})
where
    (rptc.category_id in ({CategoryIds}))
order by 
    {aOrder}
limit
    {aLimit}
offset 
    {aOffset}
