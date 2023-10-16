-- in: aLang, aParentIdRoot, CondParentIds
with recursive wrpc as (
    select
        rpc.id,
        rpc.parent_id,
        1 as deep,
        ARRAY[rpc.id] as path_id,
        rpc.sort_order || '-' || rpcl.title as sort,
        rpcl.title
    from
        ref_product0_category rpc
    left join ref_lang rlng
        on rlng.alias = '{aLang}'
    left join
        ref_product0_category_lang rpcl
        on (rpc.id = rpcl.category_id and rpcl.lang_id = rlng.id)
    where
        (rpc.enabled) and
        (rpc.parent_id = {aParentIdRoot})

    union all

    select
        rpc.id,
        rpc.parent_id,
        wrpc.deep + 1,
        wrpc.path_id  || array[rpc.id],
        wrpc.sort  || '/' || rpc.sort_order || '-' || rpcl.title,
        rpcl.title
    from
        ref_product0_category rpc
    join
        wrpc on
        (rpc.parent_id = wrpc.id)
    left join ref_lang rlng
        on rlng.alias = '{aLang}'
    left join
        ref_product0_category_lang rpcl
        on (rpc.id = rpcl.category_id and rpcl.lang_id = rlng.id)
    where
        (rpc.enabled)
),
category_products as (
    select
        rpc.cat_id,
        count(*) as products
    from
        ref_product0_to_category rptc
    left join
        ref_product rp on
        (rptc.product_id = rp.product0_id) 
    left join
        (
            select
                id,
                unnest(path_id) as cat_id
            from wrpc
        ) rpc
        on (rptc.category_id = rpc.id)
    where 
        (rp.enabled) 
    group by
        rpc.cat_id
)
select
    wrpc.id,
    wrpc.parent_id,
    wrpc.deep,
    wrpc.path_id,
    wrpc.title,
    cp.products
from
     wrpc
left join
    category_products cp on 
    (wrpc.id = cp.cat_id)
where
    (cp.products is not null)
    {CondParentIds}
order by
    wrpc.sort
