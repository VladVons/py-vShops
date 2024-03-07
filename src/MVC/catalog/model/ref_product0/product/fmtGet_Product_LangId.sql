-- fmtGet_Products_LangId.sql
-- in: aLangId, aProductId

with wt1 as (
    select
        rp.id,
        rp.idt,
        rp.cond_en,
        --coalesce(rp.idt, rp.id) as code,
        rp.tenant_id,
        rps.rest::int,
        rt.title as tenant_title,
        rpl.title,
        rpl.descr,
        rpl.features,
        rpl.meta_key,
        rpcl.title as category_title,
        array (
            select rpi.image
            from ref_product_image rpi
            where (rpi.product_id = rp.id and rpi.enabled)
            order by rpi.sort_order, rpi.image
        ) as images,
        (
            select jsonb_object_agg(ral.title, rpa.val)
            from ref_product_attr rpa
            left join ref_attr ra on (ra.id = rpa.attr_id)
            left join ref_attr_lang ral on (ral.attr_id = ra.id and ral.lang_id = {{aLangId}})
            where (rpa.product_id = {{aProductId}})
        ) as attr
    from
        ref_product rp
    left join
        reg_product_stock rps on
        (rp.id = rps.product_id)
    left join
        ref_product_lang rpl on
        (rp.id = rpl.product_id) and (rpl.lang_id = {{aLangId}})
    left join
        ref_product_to_category rptc on
        (rp.id = rptc.product_id)
    left join
        ref_product_category_lang rpcl on
        (rptc.category_id = rpcl.category_id) and (rpl.lang_id = {{aLangId}})
    left join
        ref_tenant rt on
        (rp.tenant_id = rt.id)
    where
        (rp.enabled) and
        (rp.id = {{aProductId}}) and
        (rt.enabled)
),
wt2 as (
    select
        rp.id,
        rpl.title,
        rpl.descr,
        rpl.features,
        rpl.meta_key,
        rptc.category_id,
        rpcl.title as category_title,
        array (
            select rpi.image
            from ref_product0_image rpi
            where (rpi.product_id = rp.product0_id) and (rpi.enabled)
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
        (rp.id = {{aProductId}}) and
        (rp.product0_id is not null)
)
select
    wt1.id,
    wt1.idt,
    wt1.cond_en,
    wt1.rest,
    wt1.tenant_id,
    wt1.tenant_title,
    wt1.attr,
    coalesce(wt1.title, wt2.title) as title,
    coalesce(wt1.descr, wt2.descr) as descr,
    coalesce(wt1.features, wt2.features) as features,
    coalesce(wt1.meta_key, wt2.meta_key) as meta_key,
    wt2.category_id,
    coalesce(wt1.category_title, wt2.category_title) as category_title,
    case when (cardinality(wt1.images) = 0) then wt2.images else wt1.images end as images
from
    wt1
left join wt2 on
    (wt1.id = wt2.id)
