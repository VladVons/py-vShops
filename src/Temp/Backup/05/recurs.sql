    with recursive wrpc as (
         with wrptc as (
            select 
                rptc.category_id,
                count(*) as products
            from
                ref_product_to_category rptc
            left join
                ref_product_category rpc on
                (rptc.product_id = rpc.id)
            where
                (rpc.tenant_id = 1)
            group by
                rptc.category_id
        )
        (
        select
            rpc.id,
            rpc.idt,
            rpc.parent_idt,
            1 as level,
            0 as products
        from
            ref_product_category rpc
        where
            (tenant_id = 1) and
            (parent_idt = 0)

        union all

        select
            rpc.id,
            rpc.idt,
            rpc.parent_idt,
            wrpc.level + 1,
            wrpc.products + wrptc.products
        from
            ref_product_category rpc
        join
            wrpc on
            (rpc.parent_idt = wrpc.idt)
        join
            wrptc on
            (rpc.id = wrptc.category_id)
        )
    )
    select
        *
    from
        wrpc
