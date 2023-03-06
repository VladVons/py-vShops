select
    rp.id,
    rp.idt,
    rp.tenant_id,
    rpl.title
from
    ref_product rp
left join
    ref_product_lang rpl on
    (rp.id = rpl.product_id)
where
    (rpl.lang_id = {aLangId}) and
    (rpl.title ilike all (values {Title}))
