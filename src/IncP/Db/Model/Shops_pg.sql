-- Created: 2022.12.25
-- Author: Vladimir Vons <VladVons@gmail.com>
-- License: GNU, see LICENSE for more details


-----------------------------------------------------------------------------
-- syntax --
-----------------------------------------------------------------------------
-- ALTER TYPE product_ident ADD VALUE 'new_value';
-- ALTER TABLE transaction_history ADD FOREIGN KEY (branch_id) REFERENCES banking.branch;
-- ALTER TABLE logins ADD CONSTRAINT at_least_one_of_ip4_or_ip6 CHECK ((ip_v4 IS NOT NULL) OR (ip_v6 IS NOT NULL));
-- create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- update_date         DATE,

-----------------------------------------------------------------------------
-- common enums --
-----------------------------------------------------------------------------

CREATE TYPE product_ident AS ENUM (
   'ean',
   'mpn'
);

-----------------------------------------------------------------------------
-- references. service --
-----------------------------------------------------------------------------

-- crawl---

CREATE TABLE IF NOT EXISTS ref_crawl_site(
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT FALSE,
    url                 VARCHAR(64) NOT NULL UNIQUE,
    scheme              TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ref_proxy (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOL DEFAULT FALSE,
    hostname            VARCHAR(32) NOT NULL,
    port                SMALLINT,
    login               VARCHAR(16),
    passw               VARCHAR(16)
);

-----------------------------------------------------------------------------
-- references. common tables --
-----------------------------------------------------------------------------

-- manufacturer --

CREATE TABLE IF NOT EXISTS ref_manufacturer (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(16),
    image               VARCHAR(64)
);

-- lang --

CREATE TABLE IF NOT EXISTS ref_lang (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(16),
    alias               VARCHAR(3)
);

-- currency --

CREATE TABLE IF NOT EXISTS ref_currency (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(16),
    alias               VARCHAR(3),
    code                SMALLINT,
    rate                FLOAT DEFAULT 1
);

-- address --

CREATE TABLE IF NOT EXISTS ref_country (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    deleted             BOOLEAN DEFAULT FALSE,
    title               VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS ref_city (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(32),
    country_id          INTEGER NOT NULL,
    FOREIGN KEY (country_id) REFERENCES ref_country(id)
);

CREATE TABLE IF NOT EXISTS ref_address (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    city_id             INTEGER NOT NULL,
    post_code           VARCHAR(8),
    street              VARCHAR(32),
    house               VARCHAR(4),
    room                VARCHAR(4),
    door_code           VARCHAR(8),
    FOREIGN KEY (city_id) REFERENCES ref_city(id)
);

-- customer --

CREATE TABLE IF NOT EXISTS ref_customer (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    firstname           VARCHAR(32),
    lastname            VARCHAR(32),
    phone               VARCHAR(15),
    email               VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS ref_customer_to_address (
    customer_id         INTEGER NOT NULL,
    address_id          INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES ref_customer(id),
    FOREIGN KEY (address_id) REFERENCES ref_address(id),
    PRIMARY KEY (customer_id, address_id)
);

-- company --

CREATE TABLE IF NOT EXISTS ref_company (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(32),
    address_id          INTEGER NOT NULL,
    FOREIGN KEY (address_id) REFERENCES ref_address(id)
);

CREATE TABLE IF NOT EXISTS ref_tenant (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(32),
    company_id          INTEGER NOT NULL,
    address_id          INTEGER NOT NULL,
    FOREIGN KEY (company_id) REFERENCES ref_company(id),
    FOREIGN KEY (address_id) REFERENCES ref_address(id)
);

-- product0_category --

CREATE TABLE IF NOT EXISTS ref_product0_category (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    parent_id           INTEGER NOT NULL,
    image               VARCHAR(64),
    sort_order          SMALLINT
);

CREATE TABLE IF NOT EXISTS ref_product0_category_lang (
    id                  SERIAL PRIMARY KEY,
    category_id         INTEGER NOT NULL,
    lang_id             INTEGER NOT NULL,
    title               VARCHAR(128),
    descr               TEXT,
    FOREIGN KEY (category_id) REFERENCES ref_product0_category(id),
    FOREIGN KEY (lang_id) REFERENCES ref_lang(id)
);

-- product0 --

CREATE TABLE IF NOT EXISTS ref_product0 (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    ean                 VARCHAR(13) UNIQUE,
    mpn                 VARCHAR(16) UNIQUE
);

CREATE TABLE IF NOT EXISTS ref_product0_image (
    id                  SERIAL PRIMARY KEY,
    image               VARCHAR(64) NOT NULL,
    sort_order          SMALLINT,
    product_id          INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES ref_product0(id)
);

CREATE TABLE IF NOT EXISTS ref_product0_lang (
    id                  SERIAL PRIMARY KEY,
    title               VARCHAR(128),
    descr               TEXT,
    product_id          INTEGER NOT NULL,
    lang_id             INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES ref_product0(id),
    FOREIGN KEY (lang_id) REFERENCES ref_lang(id)
);

CREATE TABLE IF NOT EXISTS ref_product0_barcode (
    id                  SERIAL PRIMARY KEY,
    code                VARCHAR(16) NOT NULL,
    ident               product_ident NOT NULL,
    product_id          INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES ref_product0(id),
    UNIQUE (code, ident)
);

CREATE TABLE IF NOT EXISTS ref_product0_to_category (
    product_id          INTEGER NOT NULL,
    category_id         INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES ref_product0(id),
    FOREIGN KEY (category_id) REFERENCES ref_product0_category(id),
    PRIMARY KEY (product_id, category_id)
);

CREATE TABLE IF NOT EXISTS ref_product0_crawl (
    id                  SERIAL PRIMARY KEY,
    url                 VARCHAR(256) NOT NULL,
    ident               product_ident NOT NULL,
    code                VARCHAR(16) NOT NULL,
    succsess            BOOLEAN NOT NULL,
    body                TEXT,
    product_id          INTEGER NOT NULL,
    crawl_site_id       INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES ref_product0(id),
    FOREIGN KEY (crawl_site_id) REFERENCES ref_crawl_site(id)
);

-----------------------------------------------------------------------------
-- references. tenant --
-----------------------------------------------------------------------------

-- price --

CREATE TABLE IF NOT EXISTS ref_price (
    id                  SERIAL PRIMARY KEY,
    title               VARCHAR(16),
    currency_id         INTEGER NOT NULL,
    tenant_id           INTEGER NOT NULL,
    FOREIGN KEY (currency_id) REFERENCES ref_currency(id),
    FOREIGN KEY (tenant_id) REFERENCES ref_tenant(id)
);

-- category --

CREATE TABLE IF NOT EXISTS ref_product_category (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    parent_id           INTEGER NOT NULL,
    image               VARCHAR(64),
    sort_order          SMALLINT,
    tenant_id           INTEGER,
    FOREIGN KEY (tenant_id) REFERENCES ref_tenant(id)
);

CREATE TABLE IF NOT EXISTS ref_product_category_lang (
    id                  SERIAL PRIMARY KEY,
    category_id         INTEGER NOT NULL,
    lang_id             INTEGER NOT NULL,
    title               VARCHAR(128),
    descr               TEXT,
    FOREIGN KEY (category_id) REFERENCES ref_product_category(id),
    FOREIGN KEY (lang_id) REFERENCES ref_lang(id)
);

-- product --

CREATE TABLE IF NOT EXISTS ref_product (
    id                  SERIAL PRIMARY KEY,
    enabled             BOOLEAN DEFAULT TRUE,
    model               VARCHAR(16),
    code                VARCHAR(10),
    is_service          BOOLEAN DEFAULT FALSE,
    product0_id         INTEGER NOT NULL,
    tenant_id           INTEGER NOT NULL,
    FOREIGN KEY (product0_id) REFERENCES ref_product0(id),
    FOREIGN KEY (tenant_id) REFERENCES ref_tenant(id),
    UNIQUE (tenant_id, code)
);

CREATE TABLE IF NOT EXISTS ref_product_price (
    id                  SERIAL PRIMARY KEY,
    product_id          INTEGER NOT NULL,
    price_id            INTEGER NOT NULL,
    price               FLOAT DEFAULT 0,
    qty                 INTEGER DEFAULT 1,
    FOREIGN KEY (product_id) REFERENCES ref_product(id),
    FOREIGN KEY (price_id) REFERENCES ref_price(id)
);

CREATE TABLE IF NOT EXISTS ref_product_price_history (
    id                  SERIAL PRIMARY KEY,
    product_price_id    INTEGER NOT NULL,
    price               FLOAT DEFAULT 0,
    FOREIGN KEY (product_price_id) REFERENCES ref_product_price(id)
);

CREATE TABLE IF NOT EXISTS ref_product_barcode (
    id                  SERIAL PRIMARY KEY,
    code                VARCHAR(13),
    ident               product_ident,
    product_id          INTEGER NOT NULL,
    tenant_id           INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES ref_product(id),
    FOREIGN KEY (tenant_id) REFERENCES ref_tenant(id),
    UNIQUE (tenant_id, code, ident)
);

CREATE TABLE IF NOT EXISTS ref_product_image (
    id                  SERIAL PRIMARY KEY,
    image               VARCHAR(64),
    sort_order          SMALLINT,
    product_id          INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES ref_product(id)
);

CREATE TABLE IF NOT EXISTS ref_product_lang (
    title               VARCHAR(128),
    descr               TEXT,
    product_id          INTEGER NOT NULL,
    lang_id             INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES ref_product(id),
    FOREIGN KEY (lang_id) REFERENCES ref_lang(id),
    PRIMARY KEY (product_id, lang_id)
);

CREATE TABLE IF NOT EXISTS ref_product_to_category (
    product_id          INTEGER NOT NULL,
    category_id         INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES ref_product(id),
    FOREIGN KEY (category_id) REFERENCES ref_product_category(id),
    PRIMARY KEY (product_id, category_id)
);

-----------------------------------------------------------------------------
-- documents --
-----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS doc_sale (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actual_date         TIMESTAMP,
    notes               VARCHAR(64),
    customer_id         INTEGER NOT NULL,
    tenant_id           INTEGER NOT NULL,
    currency_id         INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES ref_customer(id),
    FOREIGN KEY (tenant_id) REFERENCES ref_tenant(id),
    FOREIGN KEY (currency_id) REFERENCES ref_currency(id)
);
-- COMMENT ON TABLE doc_sale IS 'Документ: Продаж товару';
-- COMMENT ON COLUMN doc_sale.customer_id IS 'у кого покупаем';
-- COMMENT ON COLUMN doc_sale.tenant_id IS 'разделитель';
-- COMMENT ON COLUMN doc_sale.currency_id IS 'валюта';

CREATE TABLE IF NOT EXISTS doc_sale_table_product (
    id                  SERIAL PRIMARY KEY,
    unit_id             INTEGER NOT NULL,
    qty                 FLOAT NOT NULL,
    price               FLOAT NOT NULL,
    discount            FLOAT DEFAULT 0,
    summ                FLOAT DEFAULT 0,
    product_id          INTEGER NOT NULL,
    doc_sale_id         INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES ref_product(id),
    FOREIGN KEY (doc_sale_id) REFERENCES doc_sale(id)
);
