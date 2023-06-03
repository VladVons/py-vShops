-- get product0 with one image and size less than aSize
with wrpi as (
    select
        product_id,
        count(*)
    from 
        ref_product0_image rpi
    group by 
        product_id
    having 
        (count(product_id) = 1)
)
select 
    rpi.product_id,
    rpi.src_url,
    rpi.src_size
from
    ref_product0_image as rpi,
    wrpi
where
    (rpi.product_id in (wrpi.product_id)) and
    (rpi.src_size < {aSize})
order by
    src_size
