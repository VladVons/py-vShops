-- aOrderId
select
    dom.id as order_id,
    dom.actual_date::date,
    rc.firstname,
    rc.lastname,
    (
        select sum(qty * price)
        from doc_order_mix_table_product
        where (doc_id = {aOrderId})
    )::float as summ
from
    doc_order_mix dom
left join
    ref_customer rc on
    (dom.customer_id = rc.id)
where
    (dom.id = {aOrderId})
