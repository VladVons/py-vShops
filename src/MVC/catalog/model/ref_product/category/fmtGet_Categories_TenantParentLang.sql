-- in: aLang, aTenantId, aParentIdtRoot, CondParentIdts
with recursive wrpc as (
    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        1 as deep,
        array[rpc.idt] as path_idt,
        rpc.sort_order || '-' || rpcl.title as sort,
        rpcl.title
    from
        ref_product_category rpc
    join ref_lang rlng
        on rlng.alias = '{aLang}'
    left join
        ref_product_category_lang rpcl on
        (rpc.id = rpcl.category_id) and (rpcl.lang_id = rlng.id)
    where
        (rpc.enabled) and
        (rpc.tenant_id = {aTenantId}) and
        (rpc.parent_idt = {aParentIdtRoot})

    union all

    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        wrpc.deep + 1,
        wrpc.path_idt  || array[rpc.idt],
        wrpc.sort  || '/' || rpc.sort_order || '-' || rpcl.title,
        rpcl.title
    from
        ref_product_category rpc
    join
        wrpc on
        (rpc.parent_idt = wrpc.idt)
    join ref_lang rlng
        on rlng.alias = '{aLang}'
    left join
        ref_product_category_lang rpcl on
        (rpc.id = rpcl.category_id) and (rpcl.lang_id = rlng.id)
    where
        (rpc.enabled) and
        (rpc.tenant_id = {aTenantId})
)
select
    id,
    idt,
    parent_idt,
    deep,
    path_idt,
    title
from
     wrpc
where
    (deep between 0 and 99)
    {CondParentIdts}
order by
    sort
