-----------------------------------------------------------------------------
-- syntax --
-----------------------------------------------------------------------------
alter type product_ident add value 'new_value';
alter table transaction_history add foreign key (branch_id) references banking.branch;
alter table logins add constraint at_least_one_of_ip4_or_ip6 check ((ip_v4 is not null) or (ip_v6 is not null));

create_date         timestamp default current_timestamp
update_date         date

--very slow in function
--EXECUTE 'SELECT max(idt) + 1 FROM ' || TG_TABLE_NAME;

--https://stackoverflow.com/questions/26703476/how-to-perform-update-operations-on-columns-of-type-jsonb-in-postgres-9-4

--create extension hstore;
--drop extension hstore;

delete from ref_product;
delete from ref_product_image;
delete from ref_product_price;
delete from ref_product_category;
delete from hist_session;

---- select sequencename from pg_sequences where (sequencename like 'ref_product\_%');
ALTER SEQUENCE ref_product_id_seq RESTART 1;
ALTER SEQUENCE ref_product_image_id_seq RESTART 1;
ALTER SEQUENCE ref_product_price_id_seq RESTART 1;
ALTER SEQUENCE ref_product_category_id_seq RESTART 1;
ALTER SEQUENCE hist_session_id_seq RESTART 1;

create type val_enum as enum (
    'char',
    'int',
    'float',
    'bool'
);
