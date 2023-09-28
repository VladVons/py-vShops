-- in: aLang, CategoryIds
with recursive wrpc as (
    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        array[rpc.id] as path_id,
        array[rpcl.title::varchar] as path_title,
        array[rpc.idt] as path_idt
    from
        ref_product_category rpc
    join ref_lang rlng
        on rlng.alias = '{aLang}'
    left join
        ref_product_category_lang rpcl on
        (rpc.id = rpcl.category_id) and (rpcl.lang_id = rlng.id)
    where
        (rpc.enabled) and
        (rpc.id in ({CategoryIds}))

    union all

    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        wrpc.path_id || array[rpc.id],
        array[rpcl.title] || wrpc.path_title,
        array[rpc.idt] || wrpc.path_idt
    from
        ref_product_category rpc
    join
        wrpc on
        (wrpc.parent_idt = rpc.idt)
    join ref_lang rlng
        on rlng.alias = '{aLang}'
    left join
        ref_product_category_lang rpcl on
        (rpc.id = rpcl.category_id) and (rpcl.lang_id = rlng.id)
)
select
    path_title,
    path_idt,
    path_id[1] as id
from
    wrpc
where
    parent_idt = 0
