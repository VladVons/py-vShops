select
    rpl.product_id
from
    ref_product_lang rpl
left join
    ref_product rp on
    (rpl.product_id = rp.id)
where
    (rpl.lang_id = {aLangId}) and
    (rp.tenant_id = {aTenantId})
