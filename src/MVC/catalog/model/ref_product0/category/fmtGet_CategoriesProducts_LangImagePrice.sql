 -- in: aLangId, CategoryIds, aOrder, aLimit, aOffset
with
wt1 as (
    select
        count(*) over() as total,
        rptc.category_id as category0_id,
        rptc.product_id as product0_id,
        rp.id,
        rp.idt as product_idt,
        rp.tenant_id,
        rt.title as tenant_title,
        rpl.title,
        rpl.title as title0,
        rpcl.title as category0_title,
        (
            select rpi.image
            from ref_product0_image rpi
            where (rpi.product_id = rptc.product_id and rpi.enabled)
            order by rpi.sort_order
            limit 1
        ) as image0,
        (
            select rpi.image
            from ref_product_image rpi
            where (rpi.product_id = rp.id and rpi.enabled)
            order by rpi.sort_order
            limit 1
        ) as image,
        (
            select rpp.price
            from ref_product_price rpp
            left join ref_product_price_date rppd on (rpp.id  = rppd.product_price_id)
            left join ref_price on (rpp.price_id = ref_price.id)
            where (rpp.enabled) and (ref_price.price_en = 'sale') and
                ((rpp.product_id = rp.id) and (rppd.id is null)) or
                ((rpp.product_id = rp.id) and rppd.enabled and (now() between rppd.begin_date and rppd.end_date)) 
            order by rpp.price
            limit 1
        ) as price
    from
        ref_product0_to_category rptc
    left join
        ref_product rp on
        (rptc.product_id = rp.product0_id)
    left join
        ref_product_lang rpl
        on (rp.id = rpl.product_id and rpl.lang_id = {{aLangId}})
    left join
        ref_product0_category_lang rpcl
        on (rptc.category_id = rpcl.category_id and rpcl.lang_id = {{aLangId}})
    left join
        ref_tenant rt
        on (rp.tenant_id = rt.id)
    where
         (rptc.category_id in ({{CategoryIds}})) and
         (rp.enabled) and (rp.product0_id is not null) and (rp.product0_skip is null)
    order by
        {{aOrder}}
    limit
        {{aLimit}}
    offset
        {{aOffset}}
)
select
    wt1.total,
    wt1.category0_id as category_id,
    wt1.category0_title as category_title,
    wt1.id as product_id,
    wt1.product_idt,
    wt1.tenant_id,
    wt1.tenant_title,
    wt1.price::float,
    coalesce(wt1.title, wt1.title0) as product_title,
    coalesce(wt1.image, wt1.image0) as image
from
    wt1
