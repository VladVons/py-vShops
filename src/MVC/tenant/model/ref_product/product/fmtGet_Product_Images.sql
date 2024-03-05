-- fmtGet_Product_Images.sql
-- in: aProductId

select
    rpi.enabled,
    rpi.sort_order,
    rpi.image
from
    ref_product_image rpi
where
    (rpi.product_id = {{aProductId}})
order by
    rpi.sort_order,
    rpi.image
