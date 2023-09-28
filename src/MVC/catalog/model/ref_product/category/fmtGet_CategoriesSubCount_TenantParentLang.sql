-- in: aLang, aTenantId, aParentIdtRoot, CondParentIdts
with recursive wrpc as (
    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        1 as deep,
        ARRAY[rpc.idt] as path_idt,
        rpc.sort_order || '-' || rpcl.title as sort,
        rpcl.title
    from
        ref_product_category rpc
    left join ref_lang rlng
        on rlng.alias = '{aLang}'
    left join
        ref_product_category_lang rpcl
        on (rpc.id = rpcl.category_id and rpcl.lang_id = rlng.id)
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
    left join ref_lang rlng
        on rlng.alias = '{aLang}'
    left join
        ref_product_category_lang rpcl
        on (rpc.id = rpcl.category_id and rpcl.lang_id = rlng.id)
    where
        (rpc.enabled) and
        (rpc.tenant_id = {aTenantId})
),
category_products as (
    select
        rpc.cat_idt,
        count(*) as products
    from
        ref_product_to_category rptc
    left join
        (
            select
                id,
                unnest(path_idt) as cat_idt
            from wrpc
        ) rpc
        on (rptc.category_id = rpc.id)
    group by
        rpc.cat_idt
)

select
    wrpc.id,
    wrpc.idt,
    wrpc.parent_idt,
    wrpc.deep,
    wrpc.path_idt,
    wrpc.title,
    cp.products
from
     wrpc
left join
    category_products cp
    on (wrpc.idt = cp.cat_idt)
where
    (cp.products is not null)
    {CondParentIdts}
order by
    wrpc.sort
