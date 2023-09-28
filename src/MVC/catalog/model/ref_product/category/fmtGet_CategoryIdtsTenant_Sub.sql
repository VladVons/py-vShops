-- in: CategoryIdts, aTenantId
with recursive wrpc as (
    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        array[rpc.idt] as path_idt
    from
        ref_product_category rpc
    where
        (rpc.enabled) and
        (rpc.tenant_id = {aTenantId}) and
        (rpc.idt in ({CategoryIdts}))

    union all

    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        array[rpc.idt] || wrpc.path_idt
    from
        ref_product_category rpc
    join
        wrpc on
        (rpc.parent_idt = wrpc.idt)
    where
        (rpc.enabled) and
        (rpc.tenant_id = {aTenantId})
)
select
    wrpc.id,
    path_idt
from
    wrpc
