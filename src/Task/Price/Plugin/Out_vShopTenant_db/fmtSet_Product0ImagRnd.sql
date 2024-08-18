--fmtSet_Product0ImagRnd.sql
-- aTenantId

update ref_product0_image rpi 
set sort_order  = floor(random() * 10 + 1)::int
from ref_product0 rp0
join ref_product rp on rp.product0_id = rp0.id
where (rpi.product_id = rp0.id) and (rp.tenant_id = {aTenantId})
