-- fmtGet_LimitProducts.sql
-- in: aLimit, aOffset

select
    id,
    update_date::date
from
    ref_product
where
    enabled and (product0_id is not null)
order by
    id
limit
    {{aLimit}}
offset
    {{aOffset}}
