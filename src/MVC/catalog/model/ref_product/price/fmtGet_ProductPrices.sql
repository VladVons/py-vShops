select
    rpp.price,
    rpp.qty,
    rpp.price_id,
    rp.idt,
    rp.title,
    rppd.begin_date,
    rppd.end_date
from
    ref_product_price rpp
left join
    ref_price rp on
    (rpp.price_id = rp.id)
left join
    ref_product_price_date rppd on
    (rpp.id = rppd.product_price_id)
where
    (rpp.product_id = {aProductId}) and
    (rppd.begin_date is null or rppd.begin_date <= current_date) and
    (rppd.end_date is null or rppd.end_date >= current_date)
order by
    rpp.price desc
