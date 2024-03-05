-- fmtGet_Seo_ProductsCount.sql

select 
    count(*)
from 
    ref_product
where 
    enabled and (product0_id is not null)
