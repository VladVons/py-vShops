--fmtSet_Price_SaleRestore.sql

merge into
    ref_product_price dst
using (
    select
        rpp.id,
        rpp.product_id,
        rpp.price,
        rpp.qty,
        rp2.id as price_id
    from
        ref_product_price rpp
    join
        ref_price rp on
        rp.id = rpp.price_id
    left join
        ref_price rp2 on
        (rp2.tenant_id = rp.tenant_id) and
        (rp2.price_en = 'sale')
    where
        rpp.enabled and
        rp.price_en = 'sale_copy'
) as src
on
    (dst.product_id = src.product_id) and
    (dst.price_id = src.price_id) and
    (dst.qty = src.qty)
when matched then
    update set
        price = (src.price * (1 + (case when random() < 0.5 then -1 else 1 end) * (random() * 0.01)))::int
