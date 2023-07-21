with
wt1 as (
    insert into doc_order_mix (tenant_id, customer_id)
    values (1, 1)
    returning id
)
insert into doc_sale_table_product (doc_id, product_id, qty, price)
select wt1.id, t.product_id, t.qty, t.price from wt1,
(values (100, 2, 12.1), (101, 4, 10.6), (102, 3, 4.12)) as t(product_id, qty, price) 
