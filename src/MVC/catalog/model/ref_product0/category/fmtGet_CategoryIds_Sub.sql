-- in: CategoryIds
with recursive wrpc as (
    select
        rpc.id,
        rpc.parent_id,
        array[rpc.id] as path_id
    from
        ref_product0_category rpc
    where
        (rpc.enabled) and
        (rpc.id in ({{CategoryIds}}))

    union all

    select
        rpc.id,
        rpc.parent_id,
        array[rpc.id] || wrpc.path_id
    from
        ref_product0_category rpc
    join
        wrpc on
        (rpc.parent_id = wrpc.id)
    where
        (rpc.enabled)
)
select
    wrpc.id,
    path_id
from
    wrpc
