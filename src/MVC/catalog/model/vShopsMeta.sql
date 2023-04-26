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

--very slow in function
--EXECUTE 'SELECT max(idt) + 1 FROM ' || TG_TABLE_NAME;

--https://stackoverflow.com/questions/26703476/how-to-perform-update-operations-on-columns-of-type-jsonb-in-postgres-9-4

--create extension hstore;
--drop extension hstore;

-- delete from ref_product;
-- delete from ref_product_image;
-- delete from ref_product_price;
-- delete from ref_product_category;
-- delete from hist_session;
---- select sequencename from pg_sequences where (sequencename like 'ref_product\_%');
-- ALTER SEQUENCE ref_product_id_seq RESTART 1;
-- ALTER SEQUENCE ref_product_image_id_seq RESTART 1;
-- ALTER SEQUENCE ref_product_price_id_seq RESTART 1;
-- ALTER SEQUENCE ref_product_category_id_seq RESTART 1;

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

create type val_enum as enum (
    'char',
    'int',
    'float',
    'bool'
);

-----------------------------------------------------------------------------
-- references. user auth --
-----------------------------------------------------------------------------

create table if not exists ref_auth_group (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    title               varchar(16) not null,
    unique (title)
);

create table if not exists ref_auth_group_ext (
    id                  serial primary key,
    auth_group_id       integer not null,
    title               varchar(24) not null,
    data                text ,
    enabled             boolean default true,
    foreign key (auth_group_id) references ref_auth_group(id),
    unique (auth_group_id, title)
);

create table if not exists ref_auth (
    id                  serial primary key,
    auth_group_id       integer,
    create_date         timestamp default current_timestamp,
    valid_date          date,
    login               varchar(16) not null,
    passw               varchar(32) not null,
    enabled             boolean default true,
    foreign key (auth_group_id) references ref_auth_group(id),
    unique (login)
);

create table if not exists ref_auth_ext(
    id                  serial primary key,
    auth_id             integer not null,
    title               varchar(24) not null,
    data                text ,
    enabled             boolean default true,
    foreign key (auth_id) references ref_auth(id),
    unique (auth_id, title)
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

create table if not exists ref_query (
    path                varchar(64) not null,
    title               varchar(64) not null,
    query               text not null,
    unique (path, title)
);
COMMENT ON TABLE ref_query IS 'alternative file system queries storage';

-----------------------------------------------------------------------------
-- references. common tables --
-----------------------------------------------------------------------------

-- manufacturer --

create table if not exists ref_manufacturer (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(16) not null,
    image               varchar(64)
);

-- lang --

create table if not exists ref_lang (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(16) not null,
    alias               varchar(3)
);


-- SEO --

create table if not exists ref_seo_url (
    id                  serial primary key,
    attr                varchar(32) not null,
    val                 varchar(128) not null,
    keyword             varchar(128) not null,
    sort_order          smallint default 0,
    lang_id             integer not null,
    foreign key (lang_id) references ref_lang(id)
);
create index if not exists ref_seo_url_keyword on ref_seo_url(keyword);
create index if not exists ref_seo_url_query on ref_seo_url(attr, val);
COMMENT ON TABLE public.ref_seo_url IS 'key+value urls into SEO';

-- currency --

create table if not exists ref_currency (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(16) not null,
    alias               varchar(3) not null,
    code                smallint,
    rate                float default 1
);

-- address --

create table if not exists ref_country (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(32) not null
);

create table if not exists ref_city (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(32) not null,
    country_id          integer not null,
    foreign key (country_id) references ref_country(id)
);

create table if not exists ref_address (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    city_id             integer not null,
    post_code           varchar(8),
    street              varchar(32) not null,
    house               varchar(4) not null,
    room                varchar(4),
    door_code           varchar(8),
    foreign key (city_id) references ref_city(id)
);

-- customer --

create table if not exists ref_customer (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    firstname           varchar(32) not null,
    lastname            varchar(32) not null,
    phone               varchar(15),
    email               varchar(32) not null
);

create table if not exists ref_customer_to_address (
    customer_id         integer not null,
    address_id          integer not null,
    foreign key (customer_id) references ref_customer(id),
    foreign key (address_id) references ref_address(id),
    primary key (customer_id, address_id)
);

-- company --

create table if not exists ref_tenant (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(32) not null,
    address_id          integer not null,
    foreign key (address_id) references ref_address(id)
);
COMMENT ON TABLE ref_tenant IS 'company separator';

-- product0_category --

create table if not exists ref_product0_category (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    parent_id           integer not null,
    image               varchar(64),
    sort_order          smallint default 0
);

create table if not exists ref_product0_category_lang (
    id                  serial primary key,
    category_id         integer not null,
    lang_id             integer not null,
    title               varchar(128) not null,
    descr               text,
    meta_key            varchar(128),
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
    sort_order          smallint default 0,
    product_id          integer not null,
    foreign key (product_id) references ref_product0(id) on delete cascade
);

create table if not exists ref_product0_lang (
    id                  serial primary key,
    title               varchar(128) not null,
    descr               text,
    meta_key            varchar(128),
    product_id          integer not null,
    lang_id             integer not null,
    foreign key (product_id) references ref_product0(id) on delete cascade,
    foreign key (lang_id) references ref_lang(id)
);

create table if not exists ref_product0_barcode (
    id                  serial primary key,
    code                varchar(16) not null,
    product_en          product_enum not null,
    product_id          integer not null,
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

create table if not exists ref_conf (
    id                  serial primary key,
    attr                varchar(32) not null,
    val                 text not null,
    serialized          boolean,
    tenant_id           integer not null,
    foreign key (tenant_id) references ref_tenant(id)
);

--- module---

create table if not exists ref_module (
    id                  serial primary key,
    enabled             boolean default true,
    caption             varchar(64) not null,
    code                varchar(32) not null,
    image               varchar(64),
    conf                jsonb,
    tenant_id           integer not null,
    foreign key (tenant_id) references ref_tenant(id)
);

create table if not exists ref_module_lang (
    id                  serial primary key,
    title               varchar(256),
    intro               varchar(256),
    descr               text,
    module_id           integer not null,
    lang_id             integer not null,
    foreign key (module_id) references ref_module(id) on delete cascade,
    foreign key (lang_id) references ref_lang(id)
);

create table if not exists ref_module_group (
    id                  serial primary key,
    caption             varchar(64) not null,
    module_id           integer not null,
    foreign key (module_id) references ref_module(id) on delete cascade
);

create table if not exists ref_module_to_group (
    module_id           integer not null,
    group_id            integer not null,
    foreign key (module_id) references ref_module(id) on delete cascade,
    foreign key (group_id) references ref_module_group(id) on delete cascade,
    primary key (module_id, group_id)
);

--- layout ---

create table if not exists ref_layout (
    id                  serial primary key,
    caption             varchar(32) not null,
    route               varchar(32) not null,
    tenant_id           integer not null,
    foreign key (tenant_id) references ref_tenant(id),
    unique (tenant_id, route)
);

create table if not exists ref_layout_module (
    id                  serial primary key,
    enabled             boolean default true,
    sort_order          smallint default 0,
    place               varchar(16),
    layout_id           integer not null,
    module_id           integer not null,
    foreign key (layout_id) references ref_layout(id) on delete cascade,
    foreign key (module_id) references ref_module(id) on delete cascade,
    unique (layout_id, module_id)
);

--- news ---

create table if not exists ref_news_group (
    id                  serial primary key,
    tenant_id           integer not null,
    foreign key (tenant_id) references ref_tenant(id)
);

create table if not exists ref_news_group_lang (
    title               varchar(256) not null,
    descr               text,
    group_id            integer not null,
    lang_id             integer not null,
    foreign key (group_id) references ref_news_group(id) on delete cascade,
    foreign key (lang_id) references ref_lang(id),
    unique (group_id, lang_id)
);

create table if not exists ref_news (
    id                  serial primary key,
    enabled             boolean default true,
    create_date         timestamp default current_timestamp,
    update_date         timestamp,
    public_date         timestamp,
    tenant_id           integer not null,
    group_id            integer not null,
    foreign key (tenant_id) references ref_tenant(id)
    foreign key (group_id) references ref_news_group(id) on delete cascade,
);

create table if not exists ref_news_lang (
    title               varchar(256) not null,
    descr               text,
    meta_key            varchar(128),
    news_id             integer not null,
    lang_id             integer not null,
    foreign key (news_id) references ref_news(id) on delete cascade,
    foreign key (lang_id) references ref_lang(id),
    unique (news_id, lang_id)
);

create table if not exists ref_news_comment (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    update_date         timestamp,
    descr               text,
    news_id             integer not null,
    customer_id         integer not null,
    foreign key (news_id) references ref_news(id) on delete cascade,
    foreign key (customer_id) references ref_customer(id) on delete cascade
);

-- price --

create table if not exists ref_price (
    id                  serial primary key,
    title               varchar(16) not null,
    currency_id         integer not null,
    idt                 integer not null,
    tenant_id           integer not null,
    foreign key (currency_id) references ref_currency(id),
    foreign key (tenant_id) references ref_tenant(id),
    unique (idt, tenant_id)
);

-- category --

create table if not exists ref_product_category (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    idt                 integer not null,
    parent_idt          integer not null,
    image               varchar(64),
    sort_order          smallint default 0,
    tenant_id           integer not null,
    foreign key (tenant_id) references ref_tenant(id),
    unique (idt, tenant_id)
);
--? create index if not exists ref_product_category_tenant_idx on ref_product_category(tenant_id);

create table if not exists ref_product_category_lang (
    category_id         integer not null,
    lang_id             integer not null,
    title               varchar(128) not null,
    descr               text,
    meta_key            varchar(128),
    foreign key (category_id) references ref_product_category(id) on delete cascade,
    foreign key (lang_id) references ref_lang(id),
    unique (category_id, lang_id)
);

-- product --

create table if not exists ref_product (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    model               varchar(16),
    is_service          boolean default false,
    sort_order          smallint default 0,
    idt                 integer,
    product0_id         integer,
    tenant_id           integer not null,
    foreign key (product0_id) references ref_product0(id),
    foreign key (tenant_id) references ref_tenant(id),
    unique (tenant_id, idt)
);

create table if not exists ref_product_price (
    id                  serial primary key,
    product_id          integer not null,
    price_id            integer not null,
    price               numeric(10, 2) not null,
    qty                 smallint not null default 1,
    foreign key (product_id) references ref_product(id) on delete cascade,
    foreign key (price_id) references ref_price(id),
    unique (product_id, price_id, qty)
);

create table if not exists ref_product_price_date (
    id                  serial primary key,
    begin_date          date not null,
    end_date            date not null,
    product_price_id    integer not null,
    foreign key (product_price_id) references ref_product_price(id) on delete cascade
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
    sort_order          smallint default 0,
    product_id          integer not null,
    foreign key (product_id) references ref_product(id) on delete cascade
);
create index if not exists ref_product_image_product_id_idx on ref_product_image(product_id);

create table if not exists ref_product_lang (
    title               varchar(128) not null,
    feature             jsonb,
    descr               text,
    meta_key            varchar(128),
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

-- product attribute--

create table if not exists ref_kind (
    id                  serial primary key,
    caption             varchar(32),
    tenant_id           integer not null,
    foreign key (tenant_id) references ref_tenant(id)
);

create table if not exists ref_kind_attr (
    id                  serial primary key,
    sort_order          smallint default 0,
    reqire              boolean default false,
    val_en              val_enum,
    kind_id             integer not null,
    foreign key (kind_id) references ref_kind(id) on delete cascade
);

create table if not exists ref_kind_attr_lang (
    attr_id             integer not null,
    lang_id             integer not null,
    title               varchar(256) not null,
    foreign key (attr_id) references ref_kind_attr(id) on delete cascade,
    foreign key (lang_id) references ref_lang(id),
    unique (attr_id, lang_id)
);

create table if not exists ref_kind_attr_val (
    id                  serial primary key,
    attr_id             integer not null,
    val                 varchar(16) not null,
    foreign key (attr_id) references ref_kind_attr(id) on delete cascade
);

create table if not exists ref_kind_category (
    category_id         integer not null,
    kind_id             integer not null,
    foreign key (category_id) references ref_product_category(id) on delete cascade,
    foreign key (kind_id) references ref_kind(id) on delete cascade,
    unique (category_id, kind_id)
);

create table if not exists ref_kind_attr_product (
    val                 jsonb not null,
    product_id          integer not null,
    attr_id             integer not null,
    foreign key (product_id) references ref_product(id) on delete cascade,
    foreign key (attr_id) references ref_kind_attr(id) on delete cascade,
    unique (product_id, attr_id)
);

-----------------------------------------------------------------------------
-- history --
-----------------------------------------------------------------------------
create table if not exists hist_ref_product_price (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    price               numeric(10, 2),
    qty                 smallint,
    price_id            integer not null,
    foreign key (price_id) references ref_product_price(id) on delete cascade
);

create table if not exists hist_session (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    ip                  varchar(45),
    os                  varchar(16),
    browser             varchar(24)
);

create table if not exists hist_product_search (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    context             varchar(32) not null,
    lang_id             integer not null,
    session_id          integer not null,
    foreign key (lang_id) references ref_lang(id),
    foreign key (session_id) references hist_session(id) on delete cascade
);

create table if not exists hist_product_view (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    product_id          integer not null,
    session_id          integer not null,
    foreign key (product_id) references ref_product(id) on delete cascade,
    foreign key (session_id) references hist_session(id) on delete cascade
);

create table if not exists hist_page_view (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    url                 varchar(128),
    session_id          integer not null,
    foreign key (session_id) references hist_session(id) on delete cascade
);


-----------------------------------------------------------------------------
-- documents --
-----------------------------------------------------------------------------

create table if not exists docs (
    id                  serial primary key,
    doc_id              integer not null,
    doc_en              doc_enum not null
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
    qty                 numeric(10, 3) not null,
    price               numeric(10, 2) not null,
    discount            numeric(10, 2) default 0,
    summ                numeric(10, 2) default 0,
    product_id          integer not null,
    doc_sale_id         integer not null,
    foreign key (product_id) references ref_product(id),
    foreign key (doc_sale_id) references doc_sale(id) on delete cascade
);

--

create or replace function ref_product_price_faiu() returns trigger
as $$
begin
    if (old.price is null) or (old.price != new.price) or (old.qty != new.qty) then
        insert into hist_ref_product_price (price_id, price, qty)
        values (new.id, new.price, new.qty);
    end if;
    --raise notice '% and %', old.price, new.price;
    --return new;
    --result is ignored since this is an AFTER trigger
    return null;
end $$ language plpgsql;

create or replace trigger ref_product_price_taiu
    after insert or update of price, qty on ref_product_price
    for each row
    execute function ref_product_price_faiu();

--

create or replace function ref_product_category_fbi() returns trigger
as $$
begin
    if (new.idt is null) then
        select
            COALESCE(max(idt), 0) + 1 into new.idt
        from
            ref_product_category
        where
            tenant_id = new.tenant_id;
    end if;

    return new;
end
$$ language plpgsql;

create or replace trigger ref_product_category_tbi
    before insert on ref_product_category
    for each row
    execute procedure ref_product_category_fbi();

--

create or replace function ref_product_fbi() returns trigger
as $$
begin
    if (new.idt is null) then
        select
            COALESCE(max(idt), 0) + 1 into new.idt
        from
            ref_product
        where
            tenant_id = new.tenant_id;
    end if;

    return new;
end
$$ language plpgsql;

create or replace trigger ref_product_tbi
    before insert on ref_product
    for each row
    execute procedure ref_product_fbi();

--

create or replace function ref_price_fbi() returns trigger
as $$
begin
    if (new.idt is null) then
        select
            COALESCE(max(idt), 0) + 1 into new.idt
        from
            ref_price
        where
            tenant_id = new.tenant_id;
    end if;

    return new;
end
$$ language plpgsql;

create or replace trigger ref_price_tbi
    before insert on ref_price
    for each row
    execute procedure ref_price_fbi();
