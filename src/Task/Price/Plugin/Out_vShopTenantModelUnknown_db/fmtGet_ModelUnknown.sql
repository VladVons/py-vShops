-- fmtGet_ModelUnknown.sql

with
wt1 as (
    select
        distinct rp.model,
        rp.tenant_id
    from
        ref_product rp
    left join
        ref_product_product0 rpp on
        (rpp.product_en = 'model') and (rpp.code = rp.model)
    where
        (rp.enabled) and
        (rp.model is not null) and
        (rpp.code is null)
        -- and (tenant_id = 2)
),
wt2 as (
    select
        rpp.code as model,
        rpb.code,
        rpp.tenant_id,
        rpb.product_en
    from
        ref_product_product0 rpp
    left join
        ref_product0_barcode rpb on
        (rpp.product0_id = rpb.product_id)
    where
        (rpp.enabled) and
        (rpp.product_en = 'model')
)
select
    wt1.model,
    wt2.code,
    rt.alias
from
    wt1
left join wt2 on
    (wt1.model = wt2.model)
left join ref_tenant rt on
    (rt.id = wt1.tenant_id)
order by
    rt.alias,
    wt1.model
