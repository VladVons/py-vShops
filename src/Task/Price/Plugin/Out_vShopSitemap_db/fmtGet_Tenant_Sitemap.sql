-- in: aLimit, aOffset
with wt1 as (
    with recursive wrpc as (
        select
            rpc.tenant_id,
            rpc.parent_idt,
            array[rpc.id] as path_id,
            array[rpc.idt] as path_idt
        from
            ref_product_category rpc

        union all

        select
            rpc.tenant_id,
            rpc.parent_idt,
            wrpc.path_id || array[rpc.id],
            array[rpc.idt] || wrpc.path_idt
        from
            ref_product_category rpc
        join
            wrpc on
            (wrpc.parent_idt = rpc.idt)
    )
    select
        tenant_id,
        path_idt,
        path_id[1] as category_id
    from
        wrpc
    where
        (parent_idt = 0)
)
select
    rptc.product_id,
    rptc.category_id,
    wt1.path_idt,
    wt1.tenant_id
from
    ref_product_to_category rptc
join wt1 on
    (wt1.category_id = rptc.category_id)
order by
    tenant_id,
    category_id,
    product_id
limit
    {aLimit}
offset
    {aOffset}
