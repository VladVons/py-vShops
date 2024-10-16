-- fmtGet_Products_LangFilter.sql
-- in: aLangId, FilterRe, aOrder, aLimit, aOffset

with wt1 as (
    select
        count(*) over() as total,
        rp.id as product_id,
        rp.idt as product_idt,
        rp.product0_id,
        rptc.category_id,
        rp.tenant_id,
        rt.title as tenant_title,
        rpl.title,
        rpcl.title as category_title,
        rps.rest::int,
        (
            select rpp.price
            from ref_product_price rpp
            left join ref_price on
                (rpp.price_id = ref_price.id)
            left join ref_product_price_date rppd on 
                (rpp.id  = rppd.product_price_id)
            where (rpp.enabled) and
                (ref_price.price_en != 'purchase') and
                ((rpp.product_id = rp.id) and (rppd.id is null)) or
                ((rpp.product_id = rp.id) and rppd.enabled and (now() between rppd.begin_date and rppd.end_date))
            order by rpp.price
            limit 1
        ) as price,
        (
            select rpi.image
            from ref_product_image rpi
            where (rpi.product_id = rp.id and rpi.enabled)
            order by rpi.sort_order
            limit 1
        ) as image,
        (
            select rpi.image
            from ref_product0_image rpi
            where (rpi.product_id = rp.product0_id and rpi.enabled)
            order by rpi.sort_order
            limit 1
         ) as image0
    from
        ref_product rp
    left join
        ref_product_lang rpl on
        (rp.id = rpl.product_id) and (rpl.lang_id = {{aLangId}})
    left join
        ref_product_barcode rpb on
        (rp.id = rpb.product_id)
    left join
        ref_product_to_category rptc on
        (rp.id = rptc.product_id)
    left join
        ref_product_category_lang rpcl on
        (rptc.category_id = rpcl.category_id) and (rpl.lang_id = {{aLangId}})
    left join
        reg_product_stock rps on
        (rp.id = rps.product_id)
    left join
        ref_tenant rt on
        (rp.tenant_id = rt.id)
    where
        (rp.enabled) and
        (rp.product0_id is not null) and
        (rt.enabled) and
        (
            ((rpl.title || ' ' || rpcl.title) ilike all (values {{FilterRe}})) or
            (rp.id::varchar = '{{aFilter}}' ) or
            (rpb.code = '{{aFilter}}')
        )
    order by
        (rest > 0) desc,
        {{aOrder}}
    limit
        {{aLimit}}
    offset
        {{aOffset}}
)
select
    wt1.total,
    wt1.product_id,
    wt1.product_idt,
    wt1.category_id,
    wt1.tenant_id,
    wt1.tenant_title,
    wt1.title as product_title,
    coalesce(wt1.price, 0)::float as price,
    coalesce(wt1.image, wt1.image0) as image,
    wt1.category_title,
    wt1.rest
from
    wt1
