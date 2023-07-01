-- aTenantId, CondAttr
select
    attr,
    val,
    serialized
from
    ref_conf rc
where
    (tenant_id = {aTenantId})
    {CondAttr}
