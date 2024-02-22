-- in: aTenentId
delete from ref_product_price 
where product_id in (
    select rpp.product_id
    from ref_product_price rpp 
    left join ref_product rp on rpp.product_id = rp.id 
    where rp.tenant_id = {aTenentId}
)