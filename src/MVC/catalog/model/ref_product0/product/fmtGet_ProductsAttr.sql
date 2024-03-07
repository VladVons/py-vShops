-- fmtGet_ProductsAttr.sql
-- aLangId, ProductIds

select
    rptc0.category_id,
    rpcl0.title as category_title,
    rp.id as product_id,
    rpl.title,
    rps.rest::int,
    rp.tenant_id,
    rt.title as tenant_title,
    (
        select rpi.image
        from ref_product0_image rpi
        where (rpi.product_id = rp.product0_id and rpi.enabled)
        order by rpi.sort_order, rpi.image
        limit 1
    ) as image,
    (
        select jsonb_object_agg(ral.title, rpa.val)
        from ref_product_attr rpa
        left join ref_attr ra on (ra.id = rpa.attr_id)
        left join ref_attr_lang ral on (ral.attr_id = ra.id and ral.lang_id = {{aLangId}})
        where (rpa.product_id = rp.id)
    ) as attr,
    (
        select rpp.price
        from ref_product_price rpp
        left join ref_product_price_date rppd on (rpp.id  = rppd.product_price_id)
        left join ref_price on (rpp.price_id = ref_price.id)
        where (rpp.enabled) and (ref_price.price_en != 'purchase') and
            ((rpp.product_id = rp.id) and (rppd.id is null)) or
            ((rpp.product_id = rp.id) and rppd.enabled and (now() between rppd.begin_date and rppd.end_date))
        order by rpp.price
        limit 1
    ) as price
from
    ref_product rp
left join
    ref_product_lang rpl on
    (rpl.product_id = rp.id) and (rpl.lang_id = {{aLangId}})
left join
    ref_product0_to_category rptc0 on
    (rptc0.product_id = rp.product0_id)
left join
    ref_product0_category_lang rpcl0 on
    (rptc0.category_id = rpcl0.category_id) and (rpcl0.lang_id = {{aLangId}})
join
    ref_tenant rt on
    (rt.id = rp.tenant_id)
left join
    reg_product_stock rps on
    (rp.id = rps.product_id)
where
     (rp.id in ({{ProductIds}})) and
     (rp.enabled) and
     (rp.product0_id is not null) and
     (rt.enabled)
