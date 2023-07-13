select
    distinct(rpb.code)
    --count(distinct rpb.code)
    --count(rpb.code)
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
    (rpb.product_en = 'ean') and 
    (rpb2.code is null) and 
    (check_ean(rpb.code)) and
    (rpb.code like '48%')
order by
     rpb.code   
