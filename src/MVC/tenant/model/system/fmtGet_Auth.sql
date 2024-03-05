-- fmtGet_Auth.sql
-- aMailPhone, aPassword

select
    id,
    rttp.tenant_id
from
    ref_person rp
left join 
    ref_tenant_to_person rttp 
    on (rttp.person_id = rp.id)
where
    (rp.enabled) and
    (rp.pwd = '{{aPassword}}') and
    (rp.email = '{{aMailPhone}}' or rp.phone = '{{aMailPhone}}')
