with recursive wrpc as (
    select
        rpc.id, rpc.idt, rpc.parent_idt, rpcl.title
    from
        ref_product_category rpc
    left join
        ref_product_category_lang rpcl on
        (rpc.id = rpcl.category_id) and (rpcl.lang_id = {aLangId})
    where
        (rpc.id = {aId})

    union all

    select
        rpc.id, rpc.idt, rpc.parent_idt, rpcl.title
    from
        ref_product_category rpc
    join
        wrpc on
        (wrpc.parent_idt = rpc.idt)
    left join
        ref_product_category_lang rpcl on
        (rpc.id = rpcl.category_id) and (rpcl.lang_id = {aLangId})
)
select 
    idt,
    title
from 
    wrpc
order by
    id
