select
    rpl.product_id,
    rpl.title,
    rpl.descr,
    rpl.feature
from
    ref_product_lang rpl
where
    (rpl.product_id in ({ProductsIds})) and
    (rpl.lang_id = {aLangId})
