select
    rpb.product_id,
    rpb.tenant_id,
    rpb.code,
    rpb2.product_id as product0_id,
    rpl.title,
    rpl0.title
from
    ref_product_barcode rpb
left join
    ref_product0_barcode rpb2 on
    (rpb.product_en = rpb2.product_en) and (rpb.code = rpb2.code)
left join
    ref_product rp on
    (rpb.product_id = rp.id)
left join ref_product_lang rpl on
    (rpb.product_id = rpl.product_id)
left join ref_product0_lang rpl0 on
    (rpb2.product_id = rpl0.product_id)
where
    (rp.enabled) and
    (rp.product0_id is null) and
    (rpb.product_en = 'ean') and
    (rpb2.code is not null)
