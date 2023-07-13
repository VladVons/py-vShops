-- in: aTenantId
select
    rp.id,
    rp.tenant_id,
    rp.model,
    rptc.category_id,
    rpl.title
from
    ref_product rp
left join
    ref_product_to_category rptc on
    (rp.id = rptc.product_id)
left join
    ref_product_lang rpl on
    (rp.id = rpl.product_id)
where
    (rp.enabled) and
    (rptc.category_id is null) and 
    (rp.tenant_id = {aTenantId})
order by
    rp.id
