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
    'sale_copy',
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
    attr                varchar(32) not null,
    val                 varchar(32) not null,
    keyword             varchar(128) not null unique,
    sort_order          smallint default 0,
    primary key (attr, val)
);
COMMENT ON TABLE public.ref_seo_url IS 'key+value urls into SEO';

create table if not exists ref_seo_redirect (
    enabled             boolean default true,
    url_old             varchar(128) not null,
    url_new             varchar(128) not null,
    primary key (url_old)
);

create table if not exists ref_seo_backlink (
    id                  serial primary key,
    create_date         date default current_timestamp,
    url                 varchar(128) not null unique,
    title               varchar(128),
    descr               text,
    price               numeric(10, 2),
    dr_hrefs            int,
    publisher           varchar(32),
    note                varchar(64)
);

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

create table if not exists ref_address (
    id                  serial primary key,
    post_code           varchar(8),
    country             varchar(24) default '',
    district            varchar(24) not null,
    city                varchar(24) not null,
    street              varchar(24) not null,
    house               varchar(4) not null,
    room                varchar(4) default '',
    door_code           varchar(8),
    note                varchar(24),
    unique (country, city, street, house, room)
);

-- person --

create table if not exists ref_person (
    id                  serial primary key,
    enabled             boolean default true,
    firstname           varchar(32) not null,
    lastname            varchar(32) not null,
    middlename          varchar(32),
    birthday            date,
    gender_en           gender_enum,
    phone               varchar(15) unique,
    email               varchar(32) unique,
    image               varchar(64),
    pwd                 varchar(64),
    note                varchar(64),
    constraint ref_person_chk_email_phone check ((email is not null) or (phone is not null))
);

create table if not exists ref_person_to_address (
    person_id           integer not null references ref_person(id),
    address_id          integer not null references ref_address(id),
    primary key (person_id, address_id)
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
    icon                varchar(64),
    sort_order          smallint
);

create table if not exists ref_product0_category_lang (
    category_id         integer not null references ref_product0_category(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    title               varchar(128) not null,
    descr               text,
    meta_title          varchar(160),
    meta_key            varchar(128),
    meta_descr          varchar(160),
    primary key (category_id, lang_id)
);

create table if not exists ref_product0_category_rnd_lang (
    id                  serial primary key,
    enabled             boolean,
    descr               text,
    category_id         integer references ref_product0_category(id) on delete cascade,
    lang_id             integer not null references ref_lang(id)
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
    meta_title          varchar(160),
    meta_key            varchar(128),
    meta_descr          varchar(160),
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
    note                varchar(64),
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
    sitemap             boolean default true,
    note                varchar(32),
    route               varchar(32) not null,
    theme               varchar(16),
    common              boolean,
    tenant_id           integer not null references ref_tenant(id),
    unique (theme, tenant_id, route)
);

create table if not exists ref_layout_lang (
    title               varchar(128) not null,
    descr               text,
    meta_title          varchar(160),
    meta_key            varchar(128),
    meta_descr          varchar(160),
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
    meta_title          varchar(160),
    image               varchar(64),
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
    person_id           integer not null references ref_person(id) on delete cascade
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
    icon                varchar(64),
    sort_order          smallint,
    margin              json,
    tenant_id           integer not null references ref_tenant(id),
    attr_set_id         references ref_attr_set(id) on delete cascade,
    foreign key (parent_idt, tenant_id) references ref_product_category(idt, tenant_id) on delete cascade,
    unique (idt, tenant_id)
);
--? create index if not exists ref_product_category_tenant_idx on ref_product_category(tenant_id);

create table if not exists ref_product_category_lang (
    category_id         integer not null references ref_product_category(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    title               varchar(128) not null,
    descr               text,
    meta_title          varchar(160),
    meta_key            varchar(128),
    meta_descr          varchar(160),
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
    meta_title          varchar(160),
    meta_key            varchar(128),
    meta_descr          varchar(160),
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
    primary key (tenant_id, code, product_en)
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
    person_id           integer not null references ref_person(id) on delete cascade
);
create index if not exists ref_product_review_product_id_idx ON ref_product_review (product_id);

-- product attribute--

create table if not exists ref_attr (
    id                  serial primary key,
    alias               varchar(16) not null unique,
    val_en              val_enum not null default 'text'
);

create table if not exists ref_attr_lang (
    attr_id             integer not null references ref_attr(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    title               varchar(64) not null,
    unique (attr_id, lang_id)
);

create table if not exists ref_attr_set (
    id                  serial primary key,
    alias               varchar(16) not null unique,
    note                varchar(32)
);

create table if not exists ref_attr_set_item (
    attr_set_id         integer not null references ref_attr_set(id) on delete cascade,
    attr_id             integer not null references ref_attr(id) on delete cascade,
    reqire              boolean,
    sort_order          smallint,
    val_def             varchar(32)[],
    val_min             varchar(32),
    val_max             varchar(32),
    unique (attr_set_id, attr_id)
);

create table if not exists ref_product0_category_filter_group (
    id                  serial primary key,
    enabled             boolean default true,
    title               varchar(128) not null unique,
    category_id         integer not null references ref_product0_category(id) on delete cascade
);

create table if not exists ref_product0_category_filter (
    val                  varchar(32) not null,
    val_max              varchar(32),
    attr_id              integer not null references ref_attr(id) on delete cascade,
    filter_group_id      integer not null references ref_product0_category_filter_group(id) on delete cascade,
    unique (filter_group_id, attr_id, val)
);

create table if not exists ref_product_attr (
    val                 varchar(32),
    product_id          integer not null references ref_product(id) on delete cascade,
    attr_id             integer not null references ref_attr(id) on delete cascade,
    lang_id             integer not null references ref_lang(id),
    unique (product_id, attr_id, lang_id)
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
    browser             varchar(128),
    host                varchar(32),
    origin              text,
    uuid                varchar(36)
);

create table if not exists hist_product_search (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    context             varchar(64) not null,
    results             int,
    lang_id             integer not null references ref_lang(id),
    session_id          integer not null references hist_session(id) on delete cascade
);

create table if not exists hist_product_view (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    product_id          integer not null references ref_product(id) on delete cascade,
    session_id          integer not null references hist_session(id) on delete cascade,
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
    note                varchar(64),
    person_id           integer not null references ref_person(id)
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
    note                varchar(64),
    person_id           integer not null references ref_person(id)
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
    note                varchar(64),
    person_id           integer not null references ref_person(id),
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

