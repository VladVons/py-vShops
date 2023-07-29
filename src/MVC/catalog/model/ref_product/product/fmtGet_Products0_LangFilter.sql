-- in: aLang, FilterRe, aOrder, aLimit, aOffset
with wt1 as (
    select
        count(*) over() as total,
        rp.id as product_id,
        rp.idt as product_idt,
        rp.product0_id,
        rp.product0_skip,
        rptc.category_id,
        rp.tenant_id,
        rt.title as tenant_title,
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
            where (rpi.product_id = rp.id and rpi.enabled)
            order by rpi.sort_order
            limit 1
         ) as image
    from
        ref_product rp
    join ref_lang rlng
        on rlng.alias = '{aLang}'
    left join
        ref_product_lang rpl on
        (rp.id = rpl.product_id) and (rpl.lang_id = rlng.id)
    left join
        ref_product_barcode rpb on
        (rp.id = rpb.product_id)
    left join
        ref_product_to_category rptc on
        (rp.id = rptc.product_id)
    left join
        ref_product_category_lang rpcl on
        (rptc.category_id = rpcl.category_id) and (rpl.lang_id = rlng.id)
    left join
        ref_tenant rt on
        (rp.tenant_id = rt.id)
    where
        (rp.enabled) and
        (
            (rpl.title ilike all (values {FilterRe})) or
            (rpcl.title ilike all (values {FilterRe})) or
            (rp.idt::varchar = '{aFilter}' ) or
            (rpb.code = '{aFilter}')
        )
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
        (
            select rpi.image
            from ref_product0_image rpi
            where (rpi.product_id = wt1.product0_id) and (rpi.enabled)
            order by rpi.sort_order
            limit 1
         ) as image
    from
        wt1
    where
        (wt1.product0_id is not null) and (wt1.product0_skip is null)
)
select
    wt1.total,
    wt1.product_id,
    wt1.product_idt,
    wt1.category_id,
    wt1.tenant_id,
    wt1.tenant_title,
    wt1.title as product_title,
    wt1.price::float,
    coalesce(wt1.image, wt2.image) as image
from
    wt1
left join wt2 on
    (wt1.product_id = wt2.product_id)
