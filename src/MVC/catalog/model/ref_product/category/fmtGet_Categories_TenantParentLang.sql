with recursive wrpc as (
    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        1 as level,
        ARRAY[rpc.idt] as path
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
        wrpc.path  || array[rpc.idt]
    from
        ref_product_category rpc
    join
        wrpc on
        (rpc.parent_idt = wrpc.idt)
    where
        wrpc.level < {aDepth}
)

select
    id,
    idt,
    parent_idt,
    level,
    path,
    rpcl.title
from
    wrpc
left join
    ref_product_category_lang rpcl on
    (id = rpcl.category_id)
 where 
    rpcl.lang_id = {aLangId}
