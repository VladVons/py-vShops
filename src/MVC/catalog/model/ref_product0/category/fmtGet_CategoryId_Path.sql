-- in: aLang, CategoryIds
with recursive wrpc as (
    select
        rpc.id,
        rpc.parent_id,
        array[rpc.id] as path_id,
        array[rpcl.title::varchar] as path_title
    from
        ref_product0_category rpc
    join ref_lang rlng
        on rlng.alias = '{aLang}'
    left join
        ref_product0_category_lang rpcl on
        (rpc.id = rpcl.category_id) and (rpcl.lang_id = rlng.id)
    where
        (rpc.enabled) and
        (rpc.id in ({CategoryIds}))

    union all

    select
        rpc.id,
        rpc.parent_id,
        wrpc.path_id || array[rpc.id],
        array[rpcl.title] || wrpc.path_title
    from
        ref_product0_category rpc
    join
        wrpc on
        (wrpc.parent_id = rpc.id)
    join ref_lang rlng
        on rlng.alias = '{aLang}'
    left join
        ref_product0_category_lang rpcl on
        (rpc.id = rpcl.category_id) and (rpcl.lang_id = rlng.id)
)
select
    path_title,
    path_id,
    path_id[1] as id
from
    wrpc
where
    parent_id = 0
