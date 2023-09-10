-- aOrderId, aLang
select
    domtp.product_id as id,
    domtp.qty::float,
    domtp.price::float,
    (domtp.qty * domtp.price)::float as summ,
    rp.idt,
    rpl.title,
    (
        select
            rpi.image
        from
            ref_product_image rpi
        where
            (domtp.product_id = rpi.product_id and rpi.enabled)
        order by
            rpi.sort_order, rpi.image
        limit 1
    ) as image
from
    doc_order_mix_table_product domtp
left join
    ref_product rp on
    (domtp.product_id = rp.id)
join ref_lang rlng on
    rlng.alias = '{aLang}'
left join
    ref_product_lang rpl on
    (domtp.product_id = rpl.product_id) and (rpl.lang_id = rlng.id)
where
    (domtp.doc_id = {aOrderId})
