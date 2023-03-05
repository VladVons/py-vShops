select
    rpi.id,
    rpi.product_id,
    rpi.image
from
    ref_product_image rpi
where
    (rpi.product_id in ({ProductIds}))
order by
    rpi.sort_order
