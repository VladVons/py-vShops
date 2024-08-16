-- fmtGet_ModelEdit.sql

select
    rpi.idt,
    rpi.tenant_id,
    rpi.hash,
    rp.id,
    rp.model,
    rpl.product_id,
    rpl.lang_id,
    rpl.title,
    rpp.*
from 
    ref_product_idt rpi 
left join 
    ref_product rp on 
    rp.idt = rpi.idt and rp.tenant_id = rpi.tenant_id 
left join  
    ref_product_lang rpl on
    rpl.product_id = rp.id
left join 
    ref_product_product0 rpp on
    rpp.product0_id = rp.product0_id
where
    (rpi.tenant_id = 2)
    and rp.product0_id is not null
    --and rpl.title ilike '%dell%'
order by 
    rpi.hash 
    --rp.id 
