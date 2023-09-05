-- in: aPhone, aFirstName
insert into ref_customer (phone, firstname)
values ('{aPhone}', lower('{aFirstName}'))
on conflict (phone) do update
set firstname = excluded.firstname
returning id
