-- aTenantId, CondAttr
select
    attr,
    val,
    val_en
from
    ref_conf
where
    (tenant_id = {{aTenantId}})
    {{CondAttr}}
