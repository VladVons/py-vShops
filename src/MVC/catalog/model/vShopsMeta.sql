-- Created: 2022.12.25
-- Author: vladimir vons <vladvons@gmail.com>
-- License: gnu, see license for more details


-----------------------------------------------------------------------------
-- common enums --
-----------------------------------------------------------------------------

create type product_enum as enum (
   'ean',
   'mpn',
   'model'
);

create type doc_enum as enum (
    'doc_sale_mix',
    'doc_order_mix'
);

create type val_enum as enum (
    'int',
    'text',
    'float'
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
    auth_group_id       integer not null references ref_auth_group(id),
    title               varchar(24) not null,
    data                text ,
    enabled             boolean default true,
    unique (auth_group_id, title)
);

create table if not exists ref_auth (
    id                  serial primary key,
    auth_group_id       integer references ref_auth_group(id),
    create_date         timestamp default current_timestamp,
    valid_date          date,
    login               varchar(16) not null,
    passw               varchar(32) not null,
    enabled             boolean default true,
    unique (login)
);

create table if not exists ref_auth_ext(
    id                  serial primary key,
    auth_id             integer not null references ref_auth(id),
    title               varchar(24) not null,
    data                text ,
    enabled             boolean default true,
    unique (auth_id, title)
);

-----------------------------------------------------------------------------
-- references. service --
-----------------------------------------------------------------------------

-- crawl---

create table if not exists ref_crawl_site(
    id                  serial primary key,
    enabled             boolean default false,
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
    lang_id             integer not null references ref_lang(id)
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
    city_id             integer not null references ref_city(id),
    post_code           varchar(8),
    street              varchar(32) not null,
    house               varchar(4) not null,
    room                varchar(4),
    door_code           varchar(8)
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
    customer_id         integer not null references ref_customer(id),
    address_id          integer not null references ref_address(id),
    primary key (customer_id, address_id)
);

-- company --

create table if not exists ref_tenant (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    title               varchar(32) not null,
    address_id          integer not null references ref_address(id)
);
COMMENT ON TABLE ref_tenant IS 'company separator';

-- product0_category --

create table if not exists ref_product0_category (
    id                  serial primary key,
    enabled             boolean default true,
    parent_id           integer references ref_product0_category(id) on delete cascade,
    image               varchar(64),
    sort_order          smallint default 0
);

create table if not exists ref_product0_category_lang (
    id                  serial primary key,
    category_id         integer not null references ref_product0_category(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    title               varchar(128) not null,
    descr               text,
    meta_key            varchar(128)
);

-- product0 --

create table if not exists ref_product0 (
    id                  serial primary key,
    enabled             boolean default false
);

create table if not exists ref_product0_image (
    id                  serial primary key,
    enabled             boolean default true,
    image               varchar(64) not null,
    sort_order          smallint default 0,
    src_url             varchar(256),
    src_size            integer,
    src_date            timestamp,
    product_id          integer not null references ref_product0(id) on delete cascade,
    unique (product_id, image)
);

create table if not exists ref_product0_lang (
    id                  serial primary key,
    title               varchar(128) not null,
    descr               text,
    meta_key            varchar(128),
    product_id          integer not null references ref_product0(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    unique(product_id, lang_id)
);

create table if not exists ref_product0_barcode (
    id                  serial primary key,
    code                varchar(32) not null,
    product_en          product_enum not null,
    product_id          integer not null references ref_product0(id) on delete cascade,
    unique (code, product_en)
);

create table if not exists ref_product0_to_category (
    product_id          integer not null references ref_product0(id) on delete cascade,
    category_id         integer not null references ref_product0_category(id) on delete cascade,
    primary key (product_id, category_id)
);

create table if not exists ref_product0_crawl (
    id                  serial primary key,
    code                varchar(32),
    product_en          product_enum not null,
    url                 varchar(256),
    update_date         timestamp,
    info                json,
    crawl_site_id       integer not null references ref_crawl_site(id),
    unique (code, product_en, crawl_site_id)
);

-----------------------------------------------------------------------------
-- references. tenant --
-----------------------------------------------------------------------------

create table if not exists ref_conf (
    id                  serial primary key,
    attr                varchar(32) not null,
    val                 text not null,
    serialized          boolean,
    tenant_id           integer not null references ref_tenant(id)
);

--- module---

create table if not exists ref_module (
    id                  serial primary key,
    enabled             boolean default true,
    caption             varchar(64) not null,
    code                varchar(32) not null,
    image               varchar(64),
    conf                json,
    tenant_id           integer not null references ref_tenant(id)
);

create table if not exists ref_module_lang (
    id                  serial primary key,
    title               varchar(256),
    intro               varchar(256),
    descr               text,
    module_id           integer not null references ref_module(id) on delete cascade,
    lang_id             integer not null references ref_lang(id)
);

create table if not exists ref_module_group (
    id                  serial primary key,
    caption             varchar(64) not null,
    module_id           integer not null references ref_module(id) on delete cascade
);

create table if not exists ref_module_to_group (
    module_id           integer not null references ref_module(id) on delete cascade,
    group_id            integer not null references ref_module_group(id) on delete cascade,
    primary key (module_id, group_id)
);

--- layout ---

create table if not exists ref_layout (
    id                  serial primary key,
    caption             varchar(32) not null,
    route               varchar(32) not null,
    tenant_id           integer not null references ref_tenant(id),
    unique (tenant_id, route)
);

create table if not exists ref_layout_module (
    id                  serial primary key,
    enabled             boolean default true,
    sort_order          smallint default 0,
    place               varchar(16),
    layout_id           integer not null references ref_layout(id) on delete cascade,
    module_id           integer not null references ref_module(id) on delete cascade,
    unique (layout_id, module_id)
);

--- news ---

create table if not exists ref_news_group (
    id                  serial primary key,
    tenant_id           integer not null references ref_tenant(id)
);

create table if not exists ref_news_group_lang (
    title               varchar(256) not null,
    descr               text,
    group_id            integer not null references ref_news_group(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    unique (group_id, lang_id)
);

create table if not exists ref_news (
    id                  serial primary key,
    enabled             boolean default true,
    create_date         timestamp default current_timestamp,
    update_date         timestamp,
    public_date         timestamp,
    tenant_id           integer not null references ref_tenant(id),
    group_id            integer not null references ref_news_group(id) on delete cascade
);

create table if not exists ref_news_lang (
    title               varchar(256) not null,
    descr               text,
    meta_key            varchar(128),
    news_id             integer not null references ref_news(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    unique (news_id, lang_id)
);

create table if not exists ref_news_comment (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    update_date         timestamp,
    descr               text,
    news_id             integer not null references ref_news(id) on delete cascade,
    customer_id         integer not null references ref_customer(id) on delete cascade
);

-- price --

create table if not exists ref_price (
    id                  serial primary key,
    title               varchar(16) not null,
    idt                 integer not null,
    currency_id         integer not null references ref_currency(id),
    tenant_id           integer not null references ref_tenant(id),
    unique (idt, tenant_id)
);

-- category --

create table if not exists ref_product_category (
    id                  serial primary key,
    enabled             boolean default true,
    deleted             boolean default false,
    idt                 integer not null,
    parent_idt          integer,
    image               varchar(64),
    sort_order          smallint default 0,
    tenant_id           integer not null references ref_tenant(id),
    foreign key (parent_idt, tenant_id) references ref_product_category(idt, tenant_id) on delete cascade,
    unique (idt, tenant_id)
);
--? create index if not exists ref_product_category_tenant_idx on ref_product_category(tenant_id);

create table if not exists ref_product_category_lang (
    category_id         integer not null references ref_product_category(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    title               varchar(128) not null,
    descr               text,
    meta_key            varchar(128),
    unique (category_id, lang_id)
);

-- product --

create table if not exists ref_product (
    id                  serial primary key,
    enabled             boolean default true,
    model               varchar(64),
    is_service          boolean default false,
    sort_order          smallint default 0,
    idt                 integer,
    product0_skip       boolean,
    product0_id         integer references ref_product0(id),
    tenant_id           integer not null references ref_tenant(id),
    unique (tenant_id, idt)
);
create index if not exists ref_product_product0_id_idx ON ref_product (product0_id);

create table if not exists ref_product_price (
    id                  serial primary key,
    enabled             boolean default true,
    product_id          integer not null references ref_product(id) on delete cascade,
    price_id            integer not null references ref_price(id),
    price               numeric(10, 2) not null,
    qty                 smallint not null default 1,
    unique (product_id, price_id, qty)
);

create table if not exists ref_product_price_date (
    id                  serial primary key,
    enabled             boolean,
    begin_date          date not null,
    end_date            date not null,
    product_price_id    integer not null references ref_product_price(id) on delete cascade
);

create table if not exists ref_product_barcode (
    id                  serial primary key,
    code                varchar(32),
    product_en          product_enum not null,
    product_id          integer not null references ref_product(id) on delete cascade,
    tenant_id           integer not null references ref_tenant(id),
    unique (tenant_id, code, product_en)
);

create table if not exists ref_product_image (
    id                  serial primary key,
    enabled             boolean default true,
    image               varchar(64),
    sort_order          smallint default 0,
    src_url             varchar(128),
    src_size            integer,
    src_date            timestamp,
    product_id          integer not null references ref_product(id) on delete cascade,
    unique (product_id, image)
);
--?create index if not exists ref_product_image_product_id_idx on ref_product_image(product_id);

create table if not exists ref_product_lang (
    title               varchar(128) not null,
    summary             json,
    features            json,
    descr               text,
    meta_key            varchar(128),
    product_id          integer not null references ref_product(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    primary key (product_id, lang_id)
);

create table if not exists ref_product_to_category (
    product_id          integer not null references ref_product(id) on delete cascade,
    category_id         integer not null references ref_product_category(id) on delete cascade,
    primary key (product_id, category_id)
);

create table if not exists ref_product_idt (
    idt                 integer not null,
    hash                varchar(128) not null,
    tenant_id           integer not null references ref_tenant(id),
    primary key (tenant_id, hash)
);

create table if not exists ref_product_product0 (
    id                  serial primary key,
    enabled             boolean default true,
    code                varchar(64),
    product_en          product_enum not null,
    product0_id         integer not null references ref_product0(id) on delete cascade,
    tenant_id           integer not null references ref_tenant(id),
    unique (tenant_id, code, product_en)
);

create table if not exists ref_product_related (
    product_id          integer not null references ref_product(id) on delete cascade,
    related_id          integer not null references ref_product(id) on delete cascade,
    primary key (product_id, related_id)
);

create table if not exists ref_product_review (
    id                  serial primary key,
    enabled             boolean default true,
    descr               text,
    rating              smallint,
    create_date         timestamp default current_timestamp,
    product_id          integer not null references ref_product(id) on delete cascade,
    customer_id         integer not null references ref_customer(id) on delete cascade
);
create index if not exists ref_product_review_product_id_idx ON ref_product_review (product_id);

-- product attribute--

create table if not exists ref_kind (
    id                  serial primary key,
    caption             varchar(32),
    tenant_id           integer not null references ref_tenant(id)
);

create table if not exists ref_kind_attr (
    id                  serial primary key,
    sort_order          smallint default 0,
    reqire              boolean default false,
    val_en              val_enum,
    kind_id             integer not null references ref_kind(id) on delete cascade
);

create table if not exists ref_kind_attr_lang (
    attr_id             integer not null references ref_kind_attr(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    title               varchar(256) not null,
    unique (attr_id, lang_id)
);

create table if not exists ref_kind_attr_val (
    id                  serial primary key,
    attr_id             integer not null references ref_kind_attr(id) on delete cascade,
    val                 varchar(16) not null
);

create table if not exists ref_kind_category (
    category_id         integer not null references ref_product_category(id) on delete cascade,
    kind_id             integer not null references ref_kind(id) on delete cascade,
    unique (category_id, kind_id)
);

create table if not exists ref_kind_attr_product (
    val                 json not null,
    product_id          integer not null references ref_product(id) on delete cascade,
    attr_id             integer not null references ref_kind_attr(id) on delete cascade,
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
    price_id            integer not null references ref_product_price(id) on delete cascade
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
    lang_id             integer not null references ref_lang(id),
    session_id          integer not null references hist_session(id) on delete cascade
);

create table if not exists hist_product_view (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    product_id          integer not null references ref_product(id) on delete cascade,
    session_id          integer not null references hist_session(id) on delete cascade
);

create table if not exists hist_page_view (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    url                 varchar(128),
    session_id          integer not null references hist_session(id) on delete cascade
);


-----------------------------------------------------------------------------
-- documents --
-----------------------------------------------------------------------------
create table if not exists doc (
    id                  serial primary key,
    parent_id           integer references doc(id),
    create_date         timestamp not null default current_timestamp,
    doc_en              doc_enum not null,
    doc_id              integer not null
);

--

create table if not exists doc_order_mix (
    id                  serial primary key,
    deleted             boolean,
    actual_date         timestamp not null default current_timestamp,
    notes               varchar(64),
    customer_id         integer not null references ref_customer(id)
);

create table if not exists doc_order_mix_table_product (
    qty                 numeric(10, 3) not null,
    price               numeric(10, 2) not null,
    discount            numeric(10, 2) default 0,
    product_id          integer not null references ref_product(id),
    doc_id              integer not null references doc_order_mix(id) on delete cascade,
    primary key (product_id, doc_id)
);

--

create table if not exists doc_sale_mix (
    id                  serial primary key,
    deleted             boolean,
    actual_date         timestamp not null default current_timestamp,
    notes               varchar(64),
    customer_id         integer not null references ref_customer(id)
);

create table if not exists doc_sale_mix_table_product (
    qty                 numeric(10, 3) not null,
    price               numeric(10, 2) not null,
    discount            numeric(10, 2) default 0,
    product_id          integer not null references ref_product(id),
    doc_id              integer not null references doc_sale_mix(id) on delete cascade,
    primary key (product_id, doc_id)
);

--

create table if not exists doc_sale (
    id                  serial primary key,
    deleted             boolean,
    actual_date         timestamp not null default current_timestamp,
    notes               varchar(64),
    customer_id         integer not null references ref_customer(id),
    tenant_id           integer not null references ref_tenant(id)
);

create table if not exists doc_sale_table_product (
    qty                 numeric(10, 3) not null,
    price               numeric(10, 2) not null,
    discount            numeric(10, 2) default 0,
    product_id          integer not null references ref_product(id),
    doc_id              integer not null references doc_sale(id) on delete cascade,
    primary key (product_id, doc_id)
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
            coalesce(max(idt), 0) + 1 into new.idt
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
            coalesce(max(idt), 0) + 1 into new.idt
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
            coalesce(max(idt), 0) + 1 into new.idt
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

---

create or replace function ref_product_idt_fbi() returns trigger
as $$
begin
    if (new.idt is null) then
        select
            coalesce(max(idt), 0) + 1 into new.idt
        from
            ref_product_idt
        where
            tenant_id = new.tenant_id;
    end if;

    return new;
end
$$ language plpgsql;

create or replace trigger ref_product_idt_tbi
    before insert on ref_product_idt
    for each row
    execute procedure ref_product_idt_fbi();

---

create or replace function ref_product0_category_create(aLang int, aPath text) returns integer
as $$
declare
    ParentId int := 0;
    CategoryId int;
    CategoryName text;
begin
    foreach CategoryName in array string_to_array(aPath, '/')
    loop
        select rpc.id into CategoryId
        from ref_product0_category rpc
        left join ref_product0_category_lang rpcl on (rpc.id = rpcl.category_id)
        where (rpc.parent_id = parentid) and (rpcl.lang_id = alang) and (rpcl.title = CategoryName);

        if (CategoryId is null) then
            insert into ref_product0_category (parent_id)
            values (parentid)
            returning id into CategoryId;

            insert into ref_product0_category_lang (category_id, lang_id, title)
            values (categoryid, 1, CategoryName);
        end if;

        ParentId := CategoryId;
    end loop;

    return CategoryId;
end;
$$ language plpgsql;

---

create or replace function doc_faid() returns trigger
as $$
declare
    DocEn doc_enum;
begin
    DocEn := TG_TABLE_NAME;

    if (TG_OP = 'INSERT') then
        insert into doc (doc_en, doc_id)
        values (DocEn, new.id);
    elsif (TG_OP = 'DELETE') then
        delete from doc
        where (DocEn = doc_en) and (doc_id = old.id);
    end if;

    return null;
end
$$ language plpgsql;

--

create or replace trigger doc_taid
    after insert or delete on doc_order_mix
    for each row
    execute procedure doc_faid();

create or replace trigger doc_taid
    after insert or delete on doc_sale_mix
    for each row
    execute procedure doc_faid();

create or replace trigger doc_taid
    after insert or delete on doc_sale
    for each row
    execute procedure doc_faid();

---


-- create or replace function ref_product_image_import_fau()
-- returns trigger as $$
-- begin
--   new.update_date = now();
--   return new;
-- end;
-- $$ language plpgsql;

-- create trigger ref_product_image_import_tau
--     after update on ref_product_image_import
--     for each row
--     execute procedure ref_product_image_import_fau();

---
