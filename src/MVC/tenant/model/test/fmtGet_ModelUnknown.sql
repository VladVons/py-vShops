-- fmtGet_ModelUnknown.sql
-- aTenantId

with
wt1 as (
    select
        rp.tenant_id,
        rp.model,
        count(*),
        max(rp.id) as product_id
    from
        ref_product rp
    left join
        ref_product_product0 rpp on
        (rpp.tenant_id = rp.tenant_id) and (rpp.product_en = 'model') and (rpp.code = rp.model)
    where
        (rp.enabled) and (rp.model is not null) and (rpp.code is null) and (rp.tenant_id = {{aTenantId}})
    group by
        rp.tenant_id,
        model
    order by
        model
),
wt2 as (
    select
        rpp.code as model,
        rpb.code,
        rpb.product_en,
        rpb.product_id
    from
        ref_product_product0 rpp
    left join
        ref_product0_barcode rpb on
        (rpp.product0_id = rpb.product_id)
    where
        (rpp.enabled) and (rpp.product_en = 'model') and (rpp.tenant_id != {{aTenantId}})
)
select
    --wt1.count,
    --wt1.tenant_id,
    rt.title as tenant,
    rpcl.title as category,
    wt1.model,
    wt2.code
    --wt1.product_id
from
    wt1
left join wt2 on
    (wt1.model = wt2.model)
left join ref_tenant rt on
    (wt1.tenant_id = rt.id)
left join
    ref_product_to_category rptc on
    (rptc.product_id = wt1.product_id)
left join
    ref_product_category_lang rpcl on
    (rpcl.category_id = rptc.category_id)
order by
	tenant,
    category,
    model
