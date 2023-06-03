-- get product0 with short descr and feanures
select 
    rpl.product_id,
    rpb.code, 
    rpl.title,
    rpl.descr,
    rpl.features
from 
    ref_product0_lang rpl
left join 
    ref_product0_barcode rpb on 
    (rpb.product_id = rpl.product_id) and (rpb.product_en = 'ean')
where 
    (rpb.product_en is not null) and
    --(rpb.code like '48%') and
    (rpl.lang_id = {aLangId}) and
    ((rpl.descr is null) or (length(rpl.descr) < {aMinLen})) and 
    ((rpl.features is null) or (length(features::text) < {aMinLen}))
