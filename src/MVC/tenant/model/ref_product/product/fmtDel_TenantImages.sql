-- fmtDel_TenantImages.sql
-- in: aTenantId, CondLike

delete from
    ref_product_image rpi
using
    ref_product rp
where
    (rpi.product_id = rp.id) and
    (rp.tenant_id = {{aTenantId}}) and
    ({{CondLike}})
