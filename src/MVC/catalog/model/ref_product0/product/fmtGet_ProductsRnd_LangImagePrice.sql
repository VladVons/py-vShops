 -- in: aLang, aLimit
with
wt1 as (
    select
        rptc.category_id as category0_id,
        rptc.product_id as product_id0,
        rp.id,
        rp.idt as product_idt,
        rp.tenant_id,
        rt.title as tenant_title,
        rpl.title,
        rpl.title as title0,
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
    left join ref_lang rlng
        on rlng.alias = '{aLang}'
    left join
        ref_product0_lang rpl
        on (rptc.product_id = rpl.product_id and rpl.lang_id = rlng.id)
    left join
        ref_tenant rt
        on (rp.tenant_id = rt.id)
    where
         (rp.enabled) and (rp.product0_id is not null) and (rp.product0_skip is null)
    order by
        random()
    limit
        {aLimit}
),
wt2 as (
    with recursive wrpc as (
        select
            rpc.id,
            rpc.parent_id,
            array[rpc.id] as path_id
        from
            ref_product0_category rpc
        where
            (rpc.enabled) and
            (rpc.id in (select category0_id from wt1))

        union all

        select
            wrpc.id,
            rpc.parent_id,
            array[rpc.id] || wrpc.path_id
        from
            ref_product0_category rpc
        join
            wrpc on
            (wrpc.parent_id = rpc.id)
        where
            (rpc.enabled)
    )
    select
        wrpc.id,
        path_id
    from
        wrpc
    where
        parent_id = 0
)
select
    wt1.category0_id as category_id,
    wt1.id as product_id,
    wt1.product_idt,
    wt1.tenant_id,
    wt1.tenant_title,
    wt1.price::float,
    coalesce(wt1.title, wt1.title0) as product_title,
    coalesce(wt1.image, wt1.image0) as image,
    wt2.path_id
from
    wt1
left join
    wt2 on wt1.category0_id = wt2.id
