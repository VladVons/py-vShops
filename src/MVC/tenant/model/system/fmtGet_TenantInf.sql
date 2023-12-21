-- in: aTenantId
select 
(
    select jsonb_object_agg(price_en, id)
    from ref_price
    where (tenant_id = {{aTenantId}})
) as price,
(
    select jsonb_object_agg(alias, id)
    from ref_stock
    where (tenant_id = {{aTenantId}})
) as stock,
(
    select jsonb_object_agg(attr, val)
    from ref_conf
    where (tenant_id = {{aTenantId}})
) as conf
