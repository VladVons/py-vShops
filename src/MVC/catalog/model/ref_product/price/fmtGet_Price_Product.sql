---- price by product_id
select
    --rpp.id,
    --rpp.product_id,
    rpp.price,
    rpp.qty,
    rp.title,
    rc.alias,
    rppd.begin_date,
    rppd.end_date
from
    ref_product_price rpp
left join 
    ref_price rp on
    (rpp.price_id = rp.id)
left join 
    ref_currency rc on
    (rp.currency_id = rc.id)
left join 
    ref_product_price_date rppd on
    (rpp.id  = rppd.product_price_id)
where 
    ((rpp.product_id = 11273) and (rppd.id is null)) or 
    ((rpp.product_id = 11273) and rppd.enabled and (now() between rppd.begin_date and rppd.end_date))
order by 
    rc.alias,
    rpp.price
    