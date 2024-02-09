select 
    count(*)
from 
    ref_product
where 
    enabled and (product0_id is not null)
