select 
    rp.id,
    rp.enabled,
    rpl.title,
    rpp.price,
    rpi.image
from
    ref_product rp
left join 
    ref_product_lang rpl on 
    rp.id = rpl.product_id
left join 
    ref_product_price rpp on 
    rp.id = rpp.product_id
left join 
    ref_product_image rpi on 
    rp.id = rpi.product_id
where 
    rpl.lang_id = 1     and 
    rp.enabled
