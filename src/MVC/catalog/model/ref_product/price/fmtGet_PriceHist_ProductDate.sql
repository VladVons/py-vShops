select
    rpph.price,
    rpph.create_date
from
    ref_product_price_history rpph
left join
    ref_product_price rpp on
    (rpph.price_id = rpp.id)
where
    rpph.qty = {aQty} and
    rpph.create_date <= '{aDate}' and
    rpp.price_id = {aPriceId} and
    rpp.product_id = {aProductId}
order by
    rpph.create_date desc
limit
    1
