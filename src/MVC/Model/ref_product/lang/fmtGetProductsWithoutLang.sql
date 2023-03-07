with wrpl as (
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
)

select
    rp.id,
    rp.idt
from
    ref_product rp
left join
    wrpl on
    rp.id = wrpl.product_id
where
    (rp.tenant_id = {aTenantId}) and
    (wrpl.product_id is null)
order by
    rp.id
