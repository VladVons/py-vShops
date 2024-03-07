-- fmtAdd_OrderMix.sql
-- aCustomerId, Rows[product_id, qty, price]

with
wt1 as (
    insert into doc_order_mix (customer_id)
    values ({{aCustomerId}})
    returning id
),
wt2 as (
    insert into doc_order_mix_table_product (doc_id, product_id, qty, price)
    select wt1.id, t.product_id, t.qty, t.price from wt1,
    (values {{Rows}}) as t(product_id, qty, price)
)
select id
from wt1
