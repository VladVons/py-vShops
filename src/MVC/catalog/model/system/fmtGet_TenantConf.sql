-- aTenantId, CondAttr
select
    attr,
    val_text,
    val_json
from
    ref_conf
where
    (tenant_id = {{aTenantId}})
    {{CondAttr}}
