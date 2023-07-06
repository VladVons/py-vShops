-- in: aTenantId
with
wt1 as (
    select
        rp.model,
        count(*)
    from
        ref_product rp
    left join
        ref_product_product0 rpp on
        (rpp.tenant_id = {aTenantId}) and (rpp.product_en = 'model') and (rpp.code = rp.model)
    where
        (rp.enabled) and (rp.model is not null) and (rp.tenant_id = {aTenantId}) and (rpp.code is null)
    group by
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
        (rpp.tenant_id != {aTenantId}) and (rpp.product_en = 'model') and (rpp.enabled)
)
select
    wt1.model,
    wt2.code,
    wt2.product_id
from
    wt1
left join wt2 on
    (wt1.model = wt2.model)
