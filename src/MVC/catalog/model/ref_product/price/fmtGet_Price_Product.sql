-- fmtGet_Price_Product.sql
-- in: aProductId, aPriceType

with
wt1 as (
    select
        rpp.id,
        rpp.price_id,
        rpp.product_id,
        rpp.price,
        rpp.qty
    from
        ref_product_price rpp
    left join
        ref_product_price_date rppd on
        (rpp.id  = rppd.product_price_id) and (rppd.enabled)
    where
        (rpp.enabled) and
        (rpp.product_id = {{aProductId}}) and
        (rppd.id is null)
    ),
wt2 as (
    select
        rpp.id,
        rpp.price_id,
        rpp.product_id,
        rpp.price,
        rpp.qty,
        rppd.begin_date,
        rppd.end_date
    from
        ref_product_price rpp
    left join
        ref_product_price_date rppd on
        (rpp.id = rppd.product_price_id) and (rppd.enabled)
    where
        (rpp.enabled) and
        (rpp.product_id = {{aProductId}}) and
        (rppd.id is not null) and
        (now() between rppd.begin_date and rppd.end_date)
    )
select
    --wt1.id,
    --wt1.product_id,
    coalesce(wt1.price, 0)::float as price,
    wt1.qty,
    wt2.price::float as price_new,
    wt2.begin_date,
    wt2.end_date
from
    wt1
left join wt2 on
    (wt1.product_id = wt2.product_id) and (wt1.qty = wt2.qty)
left join
    ref_price rp on
    (wt1.price_id = rp.id)
left join
    ref_currency rc on
    (rp.currency_id = rc.id)
where 
    rp.price_en in ({{aPriceType}})
order by
     wt1.qty
