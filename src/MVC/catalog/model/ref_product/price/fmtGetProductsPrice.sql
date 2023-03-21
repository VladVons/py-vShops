select
    rpp.product_id,
    rpp.price_id,
    rpp.price,
    rpp.qty
from
    ref_product_price rpp
where
    (rpp.product_id in ({ProductIds}))
order by
    rpp.product_id,
    rpp.qty
