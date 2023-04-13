with recursive wrpc as (
    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        1 as deep,
        ARRAY[rpc.idt] as arr_path,
        rpc.sort_order || '-' || rpcl.title as sort,
        rpcl.title
    from
        ref_product_category rpc
    left join
        ref_product_category_lang rpcl 
        on (rpc.id = rpcl.category_id and rpcl.lang_id = {aLangId})
    where
        (tenant_id = {aTenantId}) and
        (parent_idt = {aParentIdtRoot})

    union all

    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        wrpc.deep + 1,
        wrpc.arr_path  || array[rpc.idt],
        wrpc.sort  || '/' || rpc.sort_order || '-' || rpcl.title,
        rpcl.title
    from
        ref_product_category rpc
    join
        wrpc on
        (rpc.parent_idt = wrpc.idt)
    left join
        ref_product_category_lang rpcl 
        on (rpc.id = rpcl.category_id and rpcl.lang_id = {aLangId})
),

category_cardinatilies as (
    select
        rpc.cat_id,
        count(*) as products
    from
        ref_product_to_category rptc
    left join
        (
            select 
                id,
                unnest(arr_path) as cat_id
            from wrpc
        ) rpc 
        on (rptc.category_id = rpc.id)
    group by
        rpc.cat_id
)

select
    wrpc.id,
    wrpc.idt,
    wrpc.parent_idt,
    wrpc.deep,
    --wrpc.arr_path,
    --wrpc.sort,
    wrpc.title,
    cc.products
from
     wrpc
left join 
    category_cardinatilies cc 
    on (wrpc.idt = cc.cat_id)
where 
    (cc.products is not null) and
    (wrpc.deep between 0 and 99)
    {CondParentIdts}
order by 
    wrpc.sort
