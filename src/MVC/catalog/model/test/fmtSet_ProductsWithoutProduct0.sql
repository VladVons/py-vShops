with wrpb as (
    select
        rpb.product_id,
        rpb2.product_id as product0_id
    from
        ref_product_barcode rpb
    left join
        ref_product0_barcode rpb2 on
        (rpb.product_en = rpb2.product_en) and (rpb.code = rpb2.code)
    left join
        ref_product rp on
        (rpb.product_id = rp.id)
    where
        (rp.enabled) and
        (rp.product0_id is null) and
        (rpb.product_en = 'ean') and
        (rpb2.code is not null)
)
update
    ref_product rp
set
    product0_id = subquery.product0_id
from (
    select
        product_id,
        product0_id
    from
        wrpb
) as subquery (id, product0_id)
where
    (rp.id = subquery.id)
returning
    rp.id, rp.product0_id
