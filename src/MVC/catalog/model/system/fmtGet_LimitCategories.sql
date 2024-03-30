-- fmtGet_LimitCategories.sql
-- in: aLang, aLimit, aOffset

with recursive wrpc as (
    select
        rpc.id,
        rpc.parent_id,
        array[rpc.id] as path_id,
        '/'::text as title
    from
        ref_product0_category rpc
    where
        (rpc.enabled) and
        (rpc.parent_id is null)

    union all

    select
        rpc.id,
        rpc.parent_id,
        array[rpc.id] || wrpc.path_id,
        rpcl.title
    from
        ref_product0_category rpc
    join
        wrpc on
        (rpc.parent_id = wrpc.id)
    left join
        ref_product0_category_lang rpcl on
        (rpc.id = rpcl.category_id) and (rpcl.lang_id = {{aLang}})
    where
        (rpc.enabled)
)
select
    count(*) over() as total,
    id,
    path_id,
    title
from
    wrpc
where 
    (parent_id is not null)
limit
    {{aLimit}}
offset
    {{aOffset}}
