-- fmtSet_Price_SaleCopy.sql

merge into
    ref_product_price dst
using (
    select
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
        (rp2.price_en = 'sale_copy')
    where
        rpp.enabled and
        rp.price_en = 'sale'
) as src
on
    (dst.product_id = src.product_id) and
    (dst.price_id = src.price_id) and
    (dst.qty = src.qty)
when matched then
    update set
        product_id = src.product_id,
        price = src.price,
        qty = src.qty,
        price_id= src.price_id
when not matched then
    insert
        (product_id, price, qty, price_id)
    values
        (src.product_id, src.price, src.qty, src.price_id)
