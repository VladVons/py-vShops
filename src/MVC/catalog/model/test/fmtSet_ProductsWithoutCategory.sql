insert into ref_product_to_category (product_id, category_id)
    select
        rp.id,
        50
    from
        ref_product rp
    left join
        ref_product_to_category rptc on
        (rp.id = rptc.product_id)
    where
        (rptc.category_id is null) and
        (rp.tenant_id = 2)
    order by
        rp.id
    returning product_id, category_id
