-- fmtGet_OrderMix.sql
-- aOrderId

select
    dom.id as order_id,
    dom.actual_date::date,
    rp.firstname,
    rp.lastname,
    (
        select sum(qty * price)
        from doc_order_mix_table_product
        where (doc_id = {{aOrderId}})
    )::float as summ
from
    doc_order_mix dom
left join
    ref_person rp on
    (dom.person_id = rp.id)
where
    (dom.id = {{aOrderId}})
