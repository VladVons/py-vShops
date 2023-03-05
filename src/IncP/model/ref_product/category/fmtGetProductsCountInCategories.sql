select
    rptc.category_id,
    count(*) as products
from
    ref_product_to_category rptc
left join
    ref_product_category rpc on
    (rptc.product_id = rpc.id)
where
    (rpc.tenant_id = {aTenantId})
group by
    rptc.category_id
