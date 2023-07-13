-- in: aTenantId
select
    rpb.product_id,
    rpb.code,
    rpl.title 
from
    ref_product_barcode rpb
left join
    ref_product0_barcode rpb2 on
    (rpb.product_en = rpb2.product_en) and (rpb.code = rpb2.code)
left join
    ref_product rp on
    (rpb.product_id = rp.id)
left join
    ref_product_lang rpl on
    (rpb.product_id = rpl.product_id)
where
    (rp.enabled) and 
    (rpb.product_en = 'ean') and 
    (rpb.tenant_id = {aTenantId}) and 
    (rpb2.code is null)
