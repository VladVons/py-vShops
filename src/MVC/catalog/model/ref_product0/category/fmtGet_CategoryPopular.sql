-- fmtGet_CategoryPopular.sql
-- in: aLangId

select
    rpc.id,
    rpc.image,
    rpc.icon,
    rpcl.title
from
     ref_product0_category rpc
left join
    ref_product0_category_lang rpcl on
    (rpcl.category_id = rpc.id and rpcl.lang_id = {{aLangId}})
where
    (rpc.enabled) and (rpc.popular)
order by
    sort_order,
    title
