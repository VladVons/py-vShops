-- in: aTenantId, Images

delete from 
    ref_product_image rpi
using 
    ref_product rp
where 
    (rpi.product_id = rp.id) and
    (rpi.image in ({{Images}})) and
    (rp.tenant_id = {{aTenantId}})
