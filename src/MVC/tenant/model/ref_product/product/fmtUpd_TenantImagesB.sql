-- in: aTenantId, Data as (product_id, image, sort_order, enabled, image_new), (...)

with src (product_id, image, sort_order, enabled, image_new) as (
    values {{Data}}
)
merge into ref_product_image as dst
using src
join ref_product rp on (src.product_id = rp.id)
on (dst.product_id = src.product_id) and (dst.image = src.image)
when matched and (rp.tenant_id = {{aTenantId}}) then
    update set sort_order = src.sort_order, enabled = src.enabled, image = src.image_new
when not matched and (rp.tenant_id = {{aTenantId}}) then
    insert (product_id, image, sort_order, enabled)
    values (src.product_id, src.image, src.sort_order, src.enabled)
