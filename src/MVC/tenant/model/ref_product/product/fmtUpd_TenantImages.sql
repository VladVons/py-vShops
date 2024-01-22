-- in: aTenantId, Data as (product_id, image), (...)

insert into 
    ref_product_image (product_id, image)
select 
    val.product_id, val.image
from 
    (values {{Data}}) as val (product_id, image)
join ref_product rp 
    on (val.product_id = rp.id)
where 
    (rp.tenant_id = {{aTenantId}})
on conflict (product_id, image) 
    do update
set 
    enabled = true
returning 
    product_id, image
