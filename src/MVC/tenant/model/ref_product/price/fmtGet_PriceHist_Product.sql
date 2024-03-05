-- fmtGet_PriceHist_Product.sql
-- in: aProductId

select
    --rpp.product_id,
    hrpp.create_date::date,
    hrpp.price::float,
    hrpp.qty,
    rp.title,
    rp.price_en,
    rc.alias
from
    ref_product_price rpp
left join
    hist_product_price hrpp on
    (rpp.id = hrpp.price_id)
left join
    ref_price rp on
    (rpp.price_id = rp.id)
left join
    ref_currency rc on
    (rp.currency_id = rc.id)
where
    (rpp.product_id = {{aProductId}}) and
    (rpp.qty = 1)
order by
    hrpp.create_date, 
    rp.price_en
