-- fmtGet_Products_PriceList.sql
-- in: aLangId

select
    rpcl.title as category,
    rp.id::varchar,
    rpl.title as product,
    rps.rest::int,
    (
        select rpp.price
        from ref_product_price rpp
        left join ref_price on
            (rpp.price_id = ref_price.id)
        left join ref_product_price_date rppd on 
            (rpp.id  = rppd.product_price_id)
        where (rpp.enabled) and
            (ref_price.price_en = 'sale') and
            ((rpp.product_id = rp.id) and (rppd.id is null)) or
            ((rpp.product_id = rp.id) and rppd.enabled and (now() between rppd.begin_date and rppd.end_date))
        order by rpp.price
        limit 1
    ) as price
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
left join
    reg_product_stock rps on
    (rp.id = rps.product_id)
where
    (rp.enabled) and
    (rp.product0_id is not null) and
    (rps.rest > 0)
order by
    category,
    product
