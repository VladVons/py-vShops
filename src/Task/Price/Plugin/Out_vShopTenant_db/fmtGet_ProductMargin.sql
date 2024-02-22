-- in: aProductIds
with wrptc as (
    select product_id, category_id
    from ref_product_to_category
    where product_id in ({aProductIds})
),
wrpcm as
(
    with recursive wrpc as (
        select
            rpc.id as category_id,
            rpc.parent_idt,
            rpc.tenant_id,
            --array[rpc.id] as path_id,
            array[rpc.margin] as margin
        from
            ref_product_category rpc
        where
            rpc.id in (
                select distinct category_id from wrptc
            )

        union all

        select
            wrpc.category_id,
            rpc.parent_idt,
            rpc.tenant_id,
            --array[rpc.id] || wrpc.path_id,
            array[rpc.margin] || wrpc.margin
        from
            ref_product_category rpc
        join
            wrpc on
            (rpc.idt = wrpc.parent_idt)
        where
            (rpc.tenant_id = wrpc.tenant_id)
    )
    select
        category_id,
        margin
    from wrpc
    where parent_idt is null
)
select
    wrptc.product_id,
    wrptc.category_id,
    wrpcm.margin
from wrptc
left join wrpcm on
    (wrptc.category_id = wrpcm.category_id)
