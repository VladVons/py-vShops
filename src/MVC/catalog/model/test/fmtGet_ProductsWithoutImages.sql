select
    rp.id
from
    ref_product rp
left join
    ref_product_image rpi on
    (rp.id = rpi.product_id)
where
    (rp.tenant_id = {aTenantId}) and
    (rpi.product_id is null)
order by
    rp.id
