-- https://habr.com/ru/post/269497
with recursive wrpc as (
    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        1 as level,
        '' || rpc.idt as path
    from
        ref_product_category rpc
    where
        (tenant_id = {aTenantId}) and
        (parent_idt = {aParentIdt})

    union all

    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        wrpc.level + 1,
        wrpc.path  || '/' || rpc.idt
    from
        ref_product_category rpc
    join
        wrpc on
        (rpc.parent_idt = wrpc.idt)
    where
        wrpc.level < {aDepth}
)

select
    *
from
    wrpc
