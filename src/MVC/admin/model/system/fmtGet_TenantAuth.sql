-- aAlias, aPasswd
select
    id
from
    ref_tenant
where
    enabled and 
    (alias = '{{aAlias}}') and 
    (passwd = '{{aPasswd}}')
