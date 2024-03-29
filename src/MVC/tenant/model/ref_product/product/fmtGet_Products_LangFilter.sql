--fmtGet_Products_LangFilter.sql
-- in: aLangId, Filter, aSearch, SearchRe, aOrder, aLimit, aOffset

with wt1 as (
    select
        count(*) over() as total,
        rp.enabled,
        rp.id,
        rp.idt,
        rps.rest::int,
        rp.product0_id,
        rptc.category_id,
        rpl.title,
        rpcl.title as category_title,
        (
            select jsonb_object_agg(ref_price.price_en, rpp.price)
            from ref_product_price rpp
            left join ref_product_price_date rppd on
                (rpp.id  = rppd.product_price_id)
            left join ref_price on
                (rpp.price_id = ref_price.id)
            where
                (rpp.enabled) and
                ((rpp.product_id = rp.id) and (rppd.id is null)) or
                ((rpp.product_id = rp.id) and rppd.enabled and (now() between rppd.begin_date and rppd.end_date))
            group by rp.id
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
        reg_product_stock rps on
        (rp.id = rps.product_id)
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
    where
        (rp.tenant_id = {{aTenantId}}) and
        (
            (rpl.title ilike all (values {{SearchRe}})) or
            (rpcl.title ilike all (values {{SearchRe}})) or
            (rp.idt::varchar = '{{aSearch}}' ) or
            (rpb.code = '{{aSearch}}')
        )
        {{Filter}}
    order by
        {{aOrder}}
    limit
        {{aLimit}}
    offset
        {{aOffset}}
)
select
    total,
    enabled,
    id,
    idt,
    rest,
    product0_id,
    category_id,
    title,
    category_title,
    price,
    image,
    image0,
    coalesce(image, image0) as image_
from 
    wt1
