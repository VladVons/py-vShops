-- fmtUpd_TenantImages.sql
-- in: aTenantId, Data as (product_id, image), (...)

insert into 
    ref_product_image (product_id, image, sort_order, enabled)
select 
    val.product_id, val.image, val.sort_order, val.enabled
from 
    (values {{Data}}) as val (product_id, image, sort_order, enabled)
join ref_product rp 
    on (val.product_id = rp.id)
where 
    (rp.tenant_id = {{aTenantId}})
on conflict (product_id, image) 
    do update
    set sort_order = excluded.sort_order, enabled = excluded.enabled
returning 
    product_id, image
