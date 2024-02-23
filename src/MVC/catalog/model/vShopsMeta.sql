-- Created: 2022.12.25
-- Author: vladimir vons <vladvons@gmail.com>
-- License: gnu, see license for more details


-----------------------------------------------------------------------------
-- common enums --
-----------------------------------------------------------------------------

create type product_enum as enum (
    'ean',
    'mpn',
    'model',
    'icecat'
);

create type doc_enum as enum (
    'doc_sale_mix',
    'doc_order_mix',
    'doc_sale',
    'doc_rest'
);

create type price_enum as enum (
    'purchase',
    'sale',
    'action'
);

create type gender_enum as enum (
    'male',
    'female'
);

create type val_enum as enum (
    'int',
    'text',
    'float',
    'json'
);

create type cond_enum as enum (
    'damaged',
    'new',
    'refurbished',
    'used'
);

-----------------------------------------------------------------------------
-- references. user auth --
-----------------------------------------------------------------------------

create table if not exists ref_auth_group (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    title               varchar(16) not null unique
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
    enabled             boolean default true,
    create_date         timestamp default current_timestamp,
    valid_date          date,
    login               varchar(16) not null unique,
    pwd                 varchar(64) not null,
    auth_group_id       integer references ref_auth_group(id)
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
    scheme              json,
    parser              varchar(16) unique,
    max_days            int2 not null default 30
);

create table if not exists ref_proxy (
    id                  serial primary key,
    enabled             bool default false,
    hostname            varchar(32) not null,
    port                smallint,
    login               varchar(16),
    pwd                 varchar(16)
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
    title               varchar(16) not null,
    image               varchar(64)
);

-- lang --

create table if not exists ref_lang (
    id                  serial primary key,
    enabled             boolean default true,
    title               varchar(16) not null,
    alias               varchar(3) not null unique
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
    title               varchar(16) not null,
    alias               varchar(3) not null unique,
    code                smallint,
    rate                numeric(10, 4) not null
);

-- address --

create table if not exists ref_country (
    id                  serial primary key,
    title               varchar(32) not null,
    alias               varchar(3) not null unique,
    code                varchar(5) unique
);

create table if not exists ref_city (
    id                  serial primary key,
    title               varchar(32) not null,
    country_id          integer not null references ref_country(id)
);

create table if not exists ref_address (
    id                  serial primary key,
    city_id             integer not null references ref_city(id),
    post_code           varchar(8),
    street              varchar(32) not null,
    house               varchar(4) not null,
    room                varchar(4),
    door_code           varchar(8)
);

-- customer --

create table if not exists ref_person (
    id                  serial primary key,
    enabled             boolean default true,
    firstname           varchar(32) not null,
    lastname            varchar(32) not null,
    birthday            date,
    gender_en           gender_enum,
    phone               varchar(15) unique,
    email               varchar(32) unique,
    image               varchar(64),
    pwd                 varchar(64),
    constraint ref_customer_chk_email_phone check ((email is not null) or (phone is not null))
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
    create_date         timestamp default current_timestamp,
    title               varchar(64) not null,
    alias               varchar(16) not null unique
);
COMMENT ON TABLE ref_tenant IS 'company separator';

create table if not exists ref_tenant_to_address (
    tenant_id           integer not null references ref_tenant(id),
    address_id          integer not null references ref_address(id),
    primary key (tenant_id, address_id)
);

create table if not exists ref_tenant_to_person (
    tenant_id           integer not null references ref_tenant(id),
    person_id           integer not null references ref_person(id),
    primary key (tenant_id, person_id)
);


-- product0_category --

create table if not exists ref_product0_category (
    id                  serial primary key,
    enabled             boolean default true,
    parent_id           integer references ref_product0_category(id) on delete cascade,
    image               varchar(64),
    sort_order          smallint default 0
);

create table if not exists ref_product0_category_lang (
    category_id         integer not null references ref_product0_category(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    title               varchar(128) not null,
    descr               text,
    meta_key            varchar(128),
    primary key (category_id, lang_id)
);

-- product0 --

create table if not exists ref_product0 (
    id                  serial primary key,
    enabled             boolean default false,
    create_date         timestamp default current_timestamp
);

create table if not exists ref_product0_image (
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
    title               varchar(128) not null,
    descr               text,
    features            json,
    meta_key            varchar(128),
    product_id          integer not null references ref_product0(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    unique(product_id, lang_id)
);

create table if not exists ref_product0_barcode (
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
    attr                varchar(32) not null,
    val                 text,
    val_en              val_enum not null,
    tenant_id           integer not null references ref_tenant(id),
    unique (tenant_id, attr)
);

--- module---

create table if not exists ref_module (
    id                  serial primary key,
    enabled             boolean default true,
    sort_order          smallint,
    code                varchar(32) not null,
    caption             varchar(64) not null,
    image               varchar(64),
    conf                json,
    tenant_id           integer not null references ref_tenant(id)
);

create table if not exists ref_module_lang (
    id                  serial primary key,
    enabled             boolean default true,
    sort_order          smallint,
    title               varchar(256),
    intro               varchar(256),
    descr               text,
    image               varchar(64),
    route               varchar(64),
    lang_id             integer not null references ref_lang(id)
);

create table if not exists ref_module_to_lang (
    module_id           integer not null references ref_module(id) on delete cascade,
    module_lang_id      integer not null references ref_module_lang(id) on delete cascade,
    primary key (module_id, module_lang_id)
);

--- layout ---

create table if not exists ref_layout (
    id                  serial primary key,
    enabled             boolean default true,
    caption             varchar(32) not null,
    route               varchar(32) not null,
    theme               varchar(16),
    common              boolean,
    tenant_id           integer not null references ref_tenant(id),
    unique (theme, tenant_id, route)
);

create table if not exists ref_layout_lang (
    title               varchar(128) not null,
    descr               text,
    meta_key            varchar(128),
    layout_id           integer not null references ref_layout(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    primary key (layout_id, lang_id)
);

create table if not exists ref_layout_module (
    enabled             boolean default true,
    sort_order          smallint default 0,
    place               varchar(16),
    layout_id           integer not null references ref_layout(id) on delete cascade,
    module_id           integer not null references ref_module(id) on delete cascade,
    primary key (layout_id, module_id)
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
    idt                 integer not null,
    title               varchar(16) not null,
    price_en            price_enum not null,
    manual              boolean,
    currency_id         integer not null references ref_currency(id),
    tenant_id           integer not null references ref_tenant(id),
    unique (idt, tenant_id)
);

-- stock --

create table if not exists ref_stock (
    id                  serial primary key,
    idt                 integer,
    title               varchar(32) not null,
    alias               varchar(16) not null default 'default',
    tenant_id           integer not null references ref_tenant(id),
    unique (idt, tenant_id),
    unique (alias, tenant_id)
);

-- category --

create table if not exists ref_product_category (
    id                  serial primary key,
    enabled             boolean default true,
    idt                 integer not null,
    parent_idt          integer,
    category0_id        integer references ref_product0_category(id),
    image               varchar(64),
    sort_order          smallint default 0,
    margin              json,
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
    create_date         timestamp default current_timestamp,
    update_date         timestamp default current_timestamp,
    model               varchar(64),
    is_service          boolean default false,
    cond_en             cond_enum,
    sort_order          smallint default 0,
    idt                 integer,
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
    code                varchar(32),
    product_en          product_enum not null,
    product_id          integer not null references ref_product(id) on delete cascade,
    tenant_id           integer not null references ref_tenant(id),
    unique (tenant_id, code, product_en)
);

create table if not exists ref_product_image (
    enabled             boolean default true,
    image               varchar(64) not null,
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
    category_idt        integer,
    primary key (tenant_id, hash),
    foreign key (idt, tenant_id) references ref_product(idt, tenant_id) on delete cascade,
    foreign key (category_idt, tenant_id) references ref_product_category(idt, tenant_id)
);

create table if not exists ref_product_product0 (
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
create table if not exists hist_product_price (
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
    browser             varchar(32)
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

create table if not exists hist_product_stock (
    id                  serial primary key,
    product_id          integer not null references ref_product(id) on delete cascade,
    doc_en              doc_enum not null,
    qty                 numeric(10, 3) not null,
    actual_date         timestamp not null
);

create table if not exists hist_currency (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    rate                numeric(10, 4) not null,
    currency_id         integer not null references ref_currency(id) on delete cascade
);

-----------------------------------------------------------------------------
-- register --
-----------------------------------------------------------------------------

create table if not exists reg_product_stock (
    product_id            integer not null references ref_product(id) on delete cascade,
    stock_id              integer not null references ref_stock(id),
    rest                  numeric(10, 3) not null,
    primary key (product_id, stock_id)
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

create or replace function ref_product_fau() returns trigger
as $$
begin
    if (old.update_date = new.update_date) then
      update ref_product
      set update_date = now()
      where id = new.id;
    end if;

    return null;
end $$ language plpgsql;

create or replace trigger ref_product_tai
    after update on ref_product
    for each row
    execute function ref_product_fau();

--

create or replace function ref_tenant_fai() returns trigger
as $$
declare
    currencyId int;
begin
    if (new.id != 0) then
        insert into ref_product_category (tenant_id, idt)
            values (new.id, 0);

        insert into ref_stock (tenant_id, title)
            values (new.id, 'default');

        select id from ref_currency where (rate = 1) into currencyId;
        insert into ref_price (tenant_id, title, price_en, currency_id)
            values (new.id, 'sale', 'sale', currencyId), 
                   (new.id, 'purchase', 'purchase', currencyId);
    end if;

    return null;
end $$ language plpgsql;

create or replace trigger ref_tenant_tai
    after insert on ref_tenant
    for each row
    execute function ref_tenant_fai();

--

create or replace function ref_product_price_faiu() returns trigger
as $$
begin
    if (old.price is null) or (old.price != new.price) or (old.qty != new.qty) then
        insert into hist_product_price (price_id, price, qty)
        values (new.id, new.price, new.qty);

        update ref_product
        set update_date = now()
        where id = new.product_id;
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

create or replace function ref_currency_faiu() returns trigger
as $$
begin
    if (old.rate != new.rate) then
        insert into hist_currency (currency_id, rate)
        values (new.id, new.rate);
    end if;
    return new;
end $$ language plpgsql;

create or replace trigger ref_currency_taiu
    after insert or update of rate on ref_currency
    for each row
    execute function ref_currency_faiu();

--

create or replace function ref_idt_inc_fbi() returns trigger
as $$
begin
    --tablename = 'ref_price'; fuck
    if (new.idt is null) then
        case
            when (TG_TABLE_NAME = 'ref_product')  then
                select coalesce(max(idt), 0) + 1 into new.idt
                from ref_product
                where (tenant_id = new.tenant_id);

            when (TG_TABLE_NAME = 'ref_product_idt')  then
                select coalesce(max(idt), 0) + 1 into new.idt
                from ref_product_idt
                where (tenant_id = new.tenant_id);

                with src (idt, tenant_id) as (
                    values (new.idt, new.tenant_id)
                )
                merge into ref_product as dst
                using src
                on (dst.idt = src.idt) and (dst.tenant_id = src.tenant_id)
                when not matched then
                    insert (idt, tenant_id)
                    values (src.idt, src.tenant_id);

            when (TG_TABLE_NAME = 'ref_product_category')  then
                select coalesce(max(idt), 0) + 1 into new.idt
                from ref_product_category
                where (tenant_id = new.tenant_id);

            when (TG_TABLE_NAME = 'ref_price')  then
                select coalesce(max(idt), 0) + 1 into new.idt
                from ref_price
                where (tenant_id = new.tenant_id);

            when (TG_TABLE_NAME = 'ref_stock')  then
                select coalesce(max(idt), 0) + 1 into new.idt
                from ref_stock
                where (tenant_id = new.tenant_id);

            else
                raise exception 'unknown table  %', TG_TABLE_NAME;
        end case;
    end if;

   return new;
end
$$ language plpgsql;

create or replace trigger ref_product_idt_inc_tbi
    before insert on ref_product
    for each row
    execute procedure ref_idt_inc_fbi();

create or replace trigger ref_product_idt_idt_inc_tbi
    before insert on ref_product_idt
    for each row
    execute procedure ref_idt_inc_fbi();

create or replace trigger ref_product_category_idt_inc_fbi
    before insert on ref_product_category
    for each row
    execute procedure ref_idt_inc_fbi();

create or replace trigger ref_price_idt_inc_tbi
    before insert on ref_price
    for each row
    execute procedure ref_idt_inc_fbi();

create or replace trigger ref_stock_idt_inc_tbi
    before insert on ref_stock
    for each row
    execute procedure ref_idt_inc_fbi();

---

create or replace function ref_product0_category_create(aLang int, aPath text) 
returns integer
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

create or replace function stock_add(a_product_ids int[], a_qtys numeric[], a_stock_id int, a_doc_en doc_enum, a_actual_date timestamp default now())
returns table (_product_id int, _rest numeric)
as $$
begin
    if (array_length(a_product_ids, 1) != array_length(a_qtys, 1)) then
        raise exception 'product array and quantity array must have same length';
    end if;

    insert into hist_product_stock (product_id, doc_en, qty, actual_date)
    select
        unnest(a_product_ids) as product_id,
        a_doc_en as doc_en,
        unnest(a_qtys) as qty,
        a_actual_date as actual_date;

    return query
        with wt1 as (
            select
                unnest(a_product_ids) as product_id,
                unnest(a_qtys) as qty
        )
        insert into reg_product_stock as rps (stock_id, product_id, rest)
        select
            a_stock_id,
            wt1.product_id,
            wt1.qty
        from wt1
        on conflict (product_id, stock_id) do update
        set rest = rps.rest + excluded.rest
        returning product_id, rest;
end;
$$language plpgsql;

--
-- select stock_set(array[421, 422], array[12, 15.12], 1, 'doc_rest')
create or replace function stock_set(a_product_ids int[], a_qtys numeric[], a_stock_id int, a_doc_en doc_enum, a_actual_date timestamp default now())
returns table (_product_id int, _rest numeric)
as $$
begin
    if (array_length(a_product_ids, 1) != array_length(a_qtys, 1)) then
        raise exception 'product array and quantity array must have same length';
    end if;

    insert into hist_product_stock as hps (product_id, doc_en, qty, actual_date)
    with wt1 as (
        select
            unnest(a_product_ids) as product_id,
            a_doc_en as doc_en,
            unnest(a_qtys) as qty,
            a_actual_date as actual_date
    )
    select wt1.*
    from wt1
    left join
        reg_product_stock rps on
        (wt1.product_id = rps.product_id) and (rps.stock_id = a_stock_id)
    where
        (wt1.qty != rps.rest) or (rps.rest is null);

    return query
        with wt1 as (
            select
                unnest(a_product_ids) as product_id,
                unnest(a_qtys) as qty
        )
        insert into reg_product_stock as rps (stock_id, product_id, rest)
        select
            a_stock_id,
            wt1.product_id,
            wt1.qty
        from wt1
        on conflict (product_id, stock_id) do update
        set rest = excluded.rest
        returning product_id, rest;
end;
$$language plpgsql;

create or replace function stock_set_tenant(a_product_id int, a_qty numeric, a_tenant_id int, a_stock_alias text default 'default')
returns void
as $$
declare 
	StockId int;
begin
	select rs.id into StockId
    from ref_stock rs
    where (rs.tenant_id = a_tenant_id) and (rs.alias = a_stock_alias);

	if (StockId is null) then
   		raise exception 'tenant_id `%` & alias `%` not exists in ref_stock', a_tenant_id, a_stock_alias;
   	end if;

   	perform stock_set(array[a_product_id], array[a_qty], StockId, 'doc_rest');
end;
$$language plpgsql;

--

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
