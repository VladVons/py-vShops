-- ProductIds
with
t_prod as (
    select
        rp.id,
        rp.tenant_id,
        rptc.category_id
    from
        ref_product rp
    left join
        ref_product_to_category rptc on
        (rp.id = rptc.product_id)
    where
        (rp.id in ({ProductIds}))
),
t_cat as
(
    with recursive wrpc as (
        select
            --rpc.id,
            --rpc.idt,
            rpc.parent_idt,
            rpc.tenant_id,
            array[rpc.idt] as path_idt,
            array[rpc.id] as path_id
        from
            ref_product_category rpc
        where
            (rpc.id in (select category_id from t_prod))

        union all

        select
            --rpc.id,
            --rpc.idt,
            rpc.parent_idt,
            rpc.tenant_id,
            array[rpc.idt] || wrpc.path_idt,
            wrpc.path_id || array[rpc.id]
        from
            ref_product_category rpc
        join
            wrpc on
            (rpc.idt = wrpc.parent_idt)
        where
            (rpc.tenant_id = wrpc.tenant_id)
    )
    select
        path_id[1] as category_id,
        (0 || path_idt) as path_idt
    from wrpc
    where (parent_idt = 0)
)
select
    t_prod.id,
    t_prod.tenant_id,
    t_prod.category_id,
    t_cat.path_idt
from t_prod
left join t_cat on
    (t_cat.category_id = t_prod.category_id)
