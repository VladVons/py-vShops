-- Created: 2022.12.25
-- Author: vladimir vons <vladvons@gmail.com>
-- License: gnu, see license for more details


-----------------------------------------------------------------------------
-- syntax --
-----------------------------------------------------------------------------
-- alter type product_ident add value 'new_value';
-- alter table transaction_history add foreign key (branch_id) references banking.branch;
-- alter table logins add constraint at_least_one_of_ip4_or_ip6 check ((ip_v4 is not null) or (ip_v6 is not null));
-- create_date         timestamp default current_timestamp
-- update_date         date,

create extension hstore;
--drop extension hstore;


-----------------------------------------------------------------------------
-- common enums --
-----------------------------------------------------------------------------

create type product_enum as enum (
   'ean',
   'mpn'
);

create type doc_enum as enum (
   'doc_sale'
);

-----------------------------------------------------------------------------
-- references. service --
-----------------------------------------------------------------------------

-- crawl---

create table if not exists ref_crawl_site(
    id                  serial primary key,
    enabled             boolean default false,
    deleted             boolean default false,
    url                 varchar(64) not null unique,
    scheme              text not null
);

create table if not exists ref_proxy (
    id                  serial primary key,
    enabled             bool default false,
    deleted             boolean default false,
    hostname            varchar(32) not null,
    port                smallint,
    login               varchar(16),
    passw               varchar(16)
);

-----------------------------------------------------------------------------
-- references. common tables --
-----------------------------------------------------------------------------

-- manufacturer --

create table if not exists ref_manufacturer (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(16),
    image               varchar(64)
);

-- lang --

create table if not exists ref_lang (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(16),
    alias               varchar(3)
);

-- currency --

create table if not exists ref_currency (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(16),
    alias               varchar(3),
    code                smallint,
    rate                float default 1
);

-- address --

create table if not exists ref_country (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(32)
);

create table if not exists ref_city (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(32),
    country_id          integer not null,
    foreign key (country_id) references ref_country(id)
);

create table if not exists ref_address (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    city_id             integer not null,
    post_code           varchar(8),
    street              varchar(32),
    house               varchar(4),
    room                varchar(4),
    door_code           varchar(8),
    foreign key (city_id) references ref_city(id)
);

-- customer --

create table if not exists ref_customer (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    firstname           varchar(32),
    lastname            varchar(32),
    phone               varchar(15),
    email               varchar(32)
);

create table if not exists ref_customer_to_address (
    customer_id         integer not null,
    address_id          integer not null,
    foreign key (customer_id) references ref_customer(id),
    foreign key (address_id) references ref_address(id),
    primary key (customer_id, address_id)
);

-- company --

create table if not exists ref_company (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(32),
    address_id          integer not null,
    foreign key (address_id) references ref_address(id)
);

create table if not exists ref_tenant (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(32),
    company_id          integer not null,
    address_id          integer not null,
    foreign key (company_id) references ref_company(id),
    foreign key (address_id) references ref_address(id)
);

-- product0_category --

create table if not exists ref_product0_category (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    parent_id           integer not null,
    image               varchar(64),
    sort_order          smallint
);

create table if not exists ref_product0_category_lang (
    id                  serial primary key,
    category_id         integer not null,
    lang_id             integer not null,
    title               varchar(128),
    descr               text,
    foreign key (category_id) references ref_product0_category(id) on delete cascade,
    foreign key (lang_id) references ref_lang(id)
);

-- product0 --

create table if not exists ref_product0 (
    id                  serial primary key,
    deleted             boolean default false,
    ean                 varchar(13) unique,
    mpn                 varchar(16) unique
);

create table if not exists ref_product0_image (
    id                  serial primary key,
    image               varchar(64) not null,
    sort_order          smallint,
    product_id          integer not null,
    foreign key (product_id) references ref_product0(id) on delete cascade
);

create table if not exists ref_product0_lang (
    id                  serial primary key,
    title               varchar(128) not null,
    descr               text,
    product_id          integer not null,
    lang_id             integer not null,
    foreign key (product_id) references ref_product0(id) on delete cascade,
    foreign key (lang_id) references ref_lang(id)
);

create table if not exists ref_product0_barcode (
    id                  serial primary key,
    code                varchar(16) not null,
    product_en          product_enum not null,
    product_id          integer not null on delete cascade,
    foreign key (product_id) references ref_product0(id) on delete cascade,
    unique (code, product_en)
);

create table if not exists ref_product0_to_category (
    product_id          integer not null,
    category_id         integer not null,
    foreign key (product_id) references ref_product0(id) on delete cascade,
    foreign key (category_id) references ref_product0_category(id) on delete cascade,
    primary key (product_id, category_id)
);

create table if not exists ref_product0_crawl (
    id                  serial primary key,
    url                 varchar(256) not null,
    product_en          product_enum not null,
    code                varchar(16) not null,
    succsess            boolean not null,
    body                text,
    product_id          integer not null,
    crawl_site_id       integer not null,
    foreign key (product_id) references ref_product0(id) on delete cascade,
    foreign key (crawl_site_id) references ref_crawl_site(id)
);

-----------------------------------------------------------------------------
-- references. tenant --
-----------------------------------------------------------------------------

-- price --

create table if not exists ref_price (
    id                  serial primary key,
    title               varchar(16),
    currency_id         integer not null,
    tenant_id           integer not null,
    foreign key (currency_id) references ref_currency(id),
    foreign key (tenant_id) references ref_tenant(id)
);

-- category --

create table if not exists ref_product_category (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    parent_id           integer not null,
    image               varchar(64),
    sort_order          smallint,
    code                varchar(10),
    tenant_id           integer,
    foreign key (tenant_id) references ref_tenant(id),
    unique (tenant_id, code)
);

create table if not exists ref_product_category_lang (
    category_id         integer not null,
    lang_id             integer not null,
    title               varchar(128),
    descr               text,
    foreign key (category_id) references ref_product_category(id) on delete cascade,
    foreign key (lang_id) references ref_lang(id),
    unique (category_id, lang)
);

-- product --

create table if not exists ref_product (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    model               varchar(16),
    is_service          boolean default false,
    code                varchar(10),
    product0_id         integer,
    tenant_id           integer not null,
    foreign key (product0_id) references ref_product0(id),
    foreign key (tenant_id) references ref_tenant(id),
    unique (tenant_id, code)
);

create table if not exists ref_product_price (
    id                  serial primary key,
    product_id          integer not null,
    price_id            integer not null,
    price               float default 0,
    qty                 integer default 1,
    foreign key (product_id) references ref_product(id) on delete cascade,
    foreign key (price_id) references ref_price(id),
    unique (product_id, price_id, qty)
);

create table if not exists ref_product_price_history (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    price               float,
    qty                 int,
    price_id            integer not null,
    foreign key (price_id) references ref_product_price(id) on delete cascade
);

create table if not exists ref_product_barcode (
    id                  serial primary key,
    code                varchar(13),
    product_en          product_enum not null,
    product_id          integer not null,
    tenant_id           integer not null,
    foreign key (product_id) references ref_product(id) on delete cascade,
    foreign key (tenant_id) references ref_tenant(id),
    unique (tenant_id, code, product_en)
);

create table if not exists ref_product_image (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    image               varchar(64),
    sort_order          smallint,
    product_id          integer not null,
    foreign key (product_id) references ref_product(id) on delete cascade
);
create index ref_product_image_product_id_idx on ref_product_image_product(product);

create table if not exists ref_product_lang (
    title               varchar(128) not null,
    feature             hstore,
    descr               text,
    product_id          integer not null,
    lang_id             integer not null,
    foreign key (product_id) references ref_product(id) on delete cascade,
    foreign key (lang_id) references ref_lang(id),
    primary key (product_id, lang_id)
);

create table if not exists ref_product_to_category (
    product_id          integer not null,
    category_id         integer not null,
    foreign key (product_id) references ref_product(id) on delete cascade,
    foreign key (category_id) references ref_product_category(id) on delete cascade,
    primary key (product_id, category_id)
);

-----------------------------------------------------------------------------
-- documents --
-----------------------------------------------------------------------------

create table if not exists docs (
    id                  serial primary key,
    doc_id              integer not null,
    doc_en              doc_enum not null,
    foreign key (doc_id, doc_en) references ref_currency(id)
);


create table if not exists doc_sale (
    id                  serial primary key,
    deleted             boolean default false,
    create_date         timestamp default current_timestamp,
    actual_date         timestamp not null,
    notes               varchar(64),
    customer_id         integer not null,
    tenant_id           integer not null,
    currency_id         integer not null,
    foreign key (customer_id) references ref_customer(id),
    foreign key (tenant_id) references ref_tenant(id),
    foreign key (currency_id) references ref_currency(id)
);

create table if not exists doc_sale_table_product (
    id                  serial primary key,
    unit_id             integer not null,
    qty                 float not null,
    price               float not null,
    discount            float default 0,
    summ                float default 0,
    product_id          integer not null,
    doc_sale_id         integer not null,
    foreign key (product_id) references ref_product(id),
    foreign key (doc_sale_id) references doc_sale(id) on delete cascade
);

create or replace function ref_product_price_update_proc()
    returns trigger
    language plpgsql
    as $$
begin
    if (old.price != new.price) or (old.qty != new.qty) then
        insert into ref_product_price_history (price_id, price, qty)
        values (old.id, new.price, new.qty);
    end if;
    --return new;

    --result is ignored since this is an AFTER trigger
    return null;
end $$;

create or replace trigger ref_product_price_update
    after update of price, qty on ref_product_price
    for each row
    execute function ref_product_price_update_proc();
