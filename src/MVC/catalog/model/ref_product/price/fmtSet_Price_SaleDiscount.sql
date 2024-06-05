-- fmtSet_Price_SaleDiscount.sql 

update ref_product_price
set price = (price * 1.1)::int
where id in (
    select
        rpp.id
    from
        ref_product_price rpp
    join
        ref_price rp on
        rp.id = rpp.price_id
    where
        rpp.enabled and
        rp.price_en = 'sale'
    )
