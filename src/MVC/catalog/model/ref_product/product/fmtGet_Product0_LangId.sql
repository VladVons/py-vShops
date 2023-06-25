with wt1 as (
    select
        rp.id,
        rp.idt,
        coalesce(rp.idt, rp.id) as code,
        rp.tenant_id,
        rt.title as tenant,
        rpl.title,
        rpl.descr,
        rpl.features,
        rpl.meta_key,
        rpcl.title as category,
        array (
            select rpi.image
            from ref_product_image rpi
            where (rpi.product_id = rp.id and rpi.enabled)
            order by rpi.sort_order, rpi.image
        ) as images
    from
        ref_product rp
    left join
        ref_product_lang rpl on
        (rp.id = rpl.product_id) and (rpl.lang_id = {aLangId})
    left join
        ref_product_to_category rptc on
        (rp.id = rptc.product_id)
    left join
        ref_product_category_lang rpcl on
        (rptc.category_id = rpcl.category_id) and (rpl.lang_id = {aLangId})
    left join
        ref_tenant rt on
        (rp.tenant_id = rt.id)
    where
        (rp.id = {aProductId})
),
wt2 as (
    select
        rp.id,
        rpl.title,
        rpl.descr,
        rpl.features,
        rpl.meta_key,
        rpcl.title as category,
        array (
            select rpi.image
            from ref_product0_image rpi
            where (rpi.product_id = rp.product0_id and rpi.enabled)
            order by rpi.sort_order, rpi.image
        ) as images
    from
        ref_product rp
    left join
        ref_product0_lang rpl on
        (rp.product0_id = rpl.product_id)
    left join
        ref_product0_to_category rptc on
        (rp.product0_id = rptc.product_id)
    left join
        ref_product0_category_lang rpcl on
        (rptc.category_id = rpcl.category_id)
    where
        (rp.id = {aProductId}) and
        (rp.product0_id is not null)
)
select
    wt1.id as product_id,
    wt1.idt,
    wt1.code,
    wt1.tenant_id,
    wt1.tenant,
    coalesce(wt1.title, wt2.title) as title,
    coalesce(wt1.descr, wt2.descr) as descr,
    coalesce(wt1.features, wt2.features) as features,
    coalesce(wt1.meta_key, wt2.meta_key) as meta_key,
    coalesce(wt1.category, wt2.category) as category,
    case when wt1.images = '{}' then wt2.images else wt1.images end as images
from wt1
    left join wt2 on
    wt1.id = wt2.id
