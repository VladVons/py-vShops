-- in: aTenantId, aProductId
select
--      rpp.product_id,
--      hrpp.price_id,
    hrpp.create_date::date,
    hrpp.price
from 
    ref_price rp
left join
    ref_product_price rpp on
    (rp.id = rpp.price_id)
left join
    hist_ref_product_price hrpp on
    (rpp.id = hrpp.price_id)
where 
    (rp.tenant_id = {{aTenantId}}) and
    (rp.idt = 1) and
    (rpp.product_id = {{aProductId}}) and
    (hrpp.qty = 1)
order by 
    hrpp.create_date
