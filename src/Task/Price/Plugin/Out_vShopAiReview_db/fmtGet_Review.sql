-- fmtGet_Products_Review.sql
-- in: aCtegories, aLimit

select
    count(*) over() as total,
    rp.id,
    rpcl.title as category_title
from
    ref_product rp
left join
    ref_product_review rpr on
    (rp.id = rpr.product_id)
left join
    ref_product_to_category rptc on
    (rp.id = rptc.product_id)
left join
    ref_product_category_lang rpcl on
    (rptc.category_id = rpcl.category_id)
left join
    reg_product_stock rps on
    (rp.id = rps.product_id)
where
    (rp.enabled) and
    (rp.product0_id is not null) and
    (rps.rest > 0) and
    (rpcl.title in ({aCategories}))
order by 
    random()
limit
    {{aLimit}}
