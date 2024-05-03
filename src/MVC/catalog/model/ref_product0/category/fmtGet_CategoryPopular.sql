-- fmtGet_CategoryPopular.sql
-- in: aLangId, aLimit

with wt1 as (
    select
        rpc.id,
        rpc.image,
        rpc.icon,
        rpcl.title
    from
         ref_product0_category rpc
    join
        ref_product0_category_lang rpcl on
        (rpcl.category_id = rpc.id) and (rpcl.lang_id = {{aLangId}})
    where
        (rpc.enabled) and (rpc.popular)
    order by
        sort_order,
        title
    limit
        10
)
select
    wt1.*,
    (
        select
            array_agg(
                array[rpc.id::varchar, rpcl.title] order by sort_order, title
            )
        from
            ref_product0_category rpc
        join ref_product0_category_lang rpcl on
            (rpcl.category_id = rpc.id) and (rpcl.lang_id = {{aLangId}})
        where
            (rpc.enabled) and (rpc.parent_id = wt1.id)
    ) as childs
from wt1
