-- fmtGet_ModelUnknown2.sql

with wt1 as (
    select rp.model
    from ref_product rp
    where rp.model is not null

    union

    select rpp.code
    from ref_product_product0 rpp
    where (rpp.product_en = 'model')
)
select
    wt1.model,
    rpb.code
    --rpp.product0_id,
    --rpl.title
from
    wt1
left join
    ref_product_product0 rpp on
    (rpp.code = wt1.model)
left join
    ref_product0_barcode rpb on
    (rpb.product_id = rpp.product0_id) and (rpb.product_en = 'icecat')
left join
    ref_product0_lang rpl on
    (rpl.product_id = rpp.product0_id)
--where
--    rpb.code is null
order by
    (rpb.code is not null) desc,
    wt1.model
