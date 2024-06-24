-- fmtGet_Category_LangId.sql
-- in: aLangId, aCategoryId

select
    rpc.id,
    rpc.image,
    rpcl.title,
    rpcl.descr,
    rpcl.meta_title,
    rpcl.meta_key,
    rpcl.meta_descr
from
    ref_product0_category rpc
left join
    ref_product0_category_lang rpcl on
    (rpcl.category_id = rpc.id) and (rpcl.lang_id = {{aLangId}})
where
    rpc.enabled and
    (rpc.id = {{aCategoryId}})
