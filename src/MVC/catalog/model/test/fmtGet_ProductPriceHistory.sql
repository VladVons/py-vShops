--in: aTenantId, aDays
select
    --rp.id,
    --max(hrpp.price_id),
    rpcl.title as category,
    rpl.title,
    array_agg(hrpp.price order by hrpp.create_date) as price,
    case
        when (min(hrpp.price) = 0) then 0.0
        else round(max(hrpp.price) / min(hrpp.price) * 100, 1) - 100
    end as rate
from 
    ref_product rp
left join
    ref_product_lang rpl on 
    (rp.id = rpl.product_id)
left join
    ref_product_to_category rptc on 
    (rp.id = rptc.product_id)
left join
    ref_product_category_lang rpcl on 
    (rptc.category_id = rpcl.category_id)
left join
    ref_product_price rpp on 
    (rp.id = rpp.product_id)
left join
    hist_ref_product_price hrpp on
    (rpp.id = hrpp.price_id)
where 
    (rp.tenant_id = {aTenantId}) and
    (hrpp.create_date > now() - interval '{aDays} day')
group by 
    rp.id,
    rpcl.title,
    rpl.title
having
    count(rp.id) > 1
    --and       (max(hrpp.price) > MIN(hrpp.price) * 1.0)
order by 
    category,
    title
