-- fmtGet_OrdersMix.sql
-- aPersonId

select
    dom.id as order_id,
    dom.actual_date::timestamp(0),
    rc.firstname,
    rc.lastname,
    (
        select sum(qty * price)
        from doc_order_mix_table_product
        where (doc_id = dom.id)
    )::float as summ
from
    doc_order_mix dom
left join
    ref_person rp on
    (dom.person_id = rp.id)
where
    (dom.person_id = {{aPersonId}})
order by
    dom.actual_date desc
