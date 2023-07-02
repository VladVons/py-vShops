-- in: aLangId, aPriceId, CategoryIds, aOrder, aLimit, aOffset
with 
wt1 as (
    select
        rptc.category_id,
        rptc.product_id,
        rp.product0_id,
        rp.product0_skip,
        rp.tenant_id,
        rpl.title,
        (
            select rpp.price
            from ref_product_price rpp
            left join ref_product_price_date rppd on (rpp.id  = rppd.product_price_id)
            where (rpp.enabled) and
                ((rpp.product_id = rp.id) and (rppd.id is null)) or
                ((rpp.product_id = rp.id) and rppd.enabled and (now() between rppd.begin_date and rppd.end_date))
            order by rpp.price
            limit 1
        ) as price,
        (
            select rpi.image
            from ref_product_image rpi
            where (rpi.product_id = rptc.product_id and rpi.enabled)
            order by rpi.sort_order
            limit 1
        ) as image
    from
        ref_product_to_category rptc
    left join
        ref_product rp on
        (rptc.product_id = rp.id and rp.enabled)
    left join
        ref_product_lang rpl
        on (rptc.product_id = rpl.product_id and rpl.lang_id = {aLangId})
    where
        (rptc.category_id in ({CategoryIds}))
    order by
        {aOrder}
    limit
        {aLimit}
    offset
        {aOffset}
),
wt2 as (
    select
        wt1.product_id,
        rpl.title,
        (
            select rpi.image
            from ref_product0_image rpi
            where (rpi.product_id = wt1.product0_id and rpi.enabled)
            order by rpi.sort_order
            limit 1
        ) as image
    from
        wt1
    left join
        ref_product0_lang rpl on
        (wt1.product0_id = rpl.product_id)
    left join
        ref_product0_to_category rptc on
        (wt1.product0_id = rptc.product_id)
    where
        (wt1.product0_id is not null) and (wt1.product0_skip is null)
)
select
    wt1.category_id,
    wt1.product_id,
    wt1.tenant_id,
    wt1.price,
    coalesce(wt1.title, wt2.title) as title,
    coalesce(wt1.image, wt2.image) as image
from
    wt1
left join wt2 on
    (wt1.product_id = wt2.product_id)
    