-- in: aTenantId
select 
    (
        select count(*)
        from ref_product 
        where (tenant_id = {{aTenantId}})
    ) as products,
    (
        select count(*)
        from ref_product 
        where (tenant_id = {{aTenantId}}) and (enabled != true)
    ) as disabled,
    (
        select count(*)
        from ref_product
        where (tenant_id = {{aTenantId}}) and (product0_id is null) 
    ) as no_product0,
    (
        select count(*)
        from ref_product rp
        left join ref_product_price rpp 
            on (rpp.product_id = rp.id) 
        left join ref_price  
            on (ref_price.id = rpp.price_id) and (ref_price.price_en = 'sale') 
        where (rp.tenant_id = {{aTenantId}}) and (rpp.id is null)
    ) as no_price
