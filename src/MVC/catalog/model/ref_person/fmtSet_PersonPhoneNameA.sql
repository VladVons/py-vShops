-- fmtSet_PersonPhoneName.sql
-- in: aPhone, aFirstName

insert into ref_person
    (phone, firstname, lastname, middlename)
values (
    '{{aPhone}}',
    lower('{{aFirstName}}'),
    lower('{{aLastName}}'),
    lower('{{aMiddleName}}')
)
on
    conflict (phone) do update
set
    firstname = excluded.firstname,
    lastname = excluded.lastname,
    middlename = excluded.middlename
returning id
