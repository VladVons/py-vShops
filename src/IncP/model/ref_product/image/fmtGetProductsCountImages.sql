select
    rp.id,
    count(*) as images
from
    ref_product rp
right join
    ref_product_image rpi on
    (rp.id = rpi.product_id)
where
    (rp.tenant_id = {aTenantId})
group by
    rp.id
order by
    images
