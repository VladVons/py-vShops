-- in: aLang, FilterRe
select
    rpl.title
from
    ref_product rp
join ref_lang rlng
    on rlng.alias = '{aLang}'
left join
    ref_product_lang rpl on
    (rp.id = rpl.product_id) and (rpl.lang_id = rlng.id)
left join
    ref_product_to_category rptc on
    (rp.id = rptc.product_id)
left join
    ref_product_category_lang rpcl on
    (rptc.category_id = rpcl.category_id) and (rpl.lang_id = rlng.id)
where
    (rp.enabled) and
    (rp.product0_id is not null) and (rp.product0_skip is null) and
    (
        (rpl.title ilike all (values {FilterRe})) or
        (rpcl.title ilike all (values {FilterRe}))
    )
limit
    10
