-- in: aLangId, FilterRe
select
    rpl.title
from
    ref_product rp
left join
    ref_product_lang rpl on
    (rp.id = rpl.product_id) and (rpl.lang_id = {{aLangId}})
left join
    ref_product_to_category rptc on
    (rp.id = rptc.product_id)
left join
    ref_product_category_lang rpcl on
    (rptc.category_id = rpcl.category_id) and (rpl.lang_id = {{aLangId}})
where
    (rp.enabled) and
    (rp.product0_id is not null) and
    (
        (rpl.title ilike all (values {{FilterRe}})) or
        (rpcl.title ilike all (values {{FilterRe}}))
    )
limit
    10
