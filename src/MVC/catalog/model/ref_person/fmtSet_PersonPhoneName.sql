-- fmtSet_PersonPhoneName.sql
-- in: aPhone, aFirstName

with src (phone, firstname, lastname, middlename) as (
    values (
        '{{aPhone}}',
        lower('{{aFirstName}}'),
        lower('{{aLastName}}'),
        lower('{{aMiddleName}}')
    )
)
merge into ref_person as dst
using src
on (dst.phone = src.phone)
when matched then
update set
    firstname = src.firstname,
    lastname = src.lastname,
    middlename = src.middlename
when not matched then
    insert (phone, firstname, lastname, middlename)
    values (src.phone, src.firstname, src.lastname, src.middlename);

-- ToDo. 2 queries
select id
from ref_person rp 
where (phone = '{{aPhone}}')
