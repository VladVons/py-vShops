-- in: aPhone, aFirstName
select
    id
from
    ref_customer rc
where
    (rc.phone = '{aPhone}') and
    (rc.firstname = lower('{aFirstName}'))
