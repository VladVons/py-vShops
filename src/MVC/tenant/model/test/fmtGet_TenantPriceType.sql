-- in: aTenantId
select 
    rp.id,
    rp.model,
    rp.tenant_id,
    rpp.id as priceId,
    rpp.price,
    ref_price.price_en
from 
    ref_product rp
left join 
    ref_product_price rpp on
    rp.id = rpp.product_id 
left join 
    ref_price on 
    rpp.price_id = ref_price.id 
where 
    ref_price.price_en = 'sale' and
    rp.tenant_id = 2
