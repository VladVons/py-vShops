-- Created: 2022.12.25
-- Author: Vladimir Vons <VladVons@gmail.com>
-- License: GNU, see LICENSE for more details


-----------
-- common enums --
-----------


CREATE TYPE product_ident AS ENUM (
	'ean13', 
	'mpn'
);
-- ALTER TYPE product_ident ADD VALUE 'new_value';


-----------
-- common tables --
-----------

-- manufacturer --

CREATE TABLE IF NOT EXISTS ref_manufacturer (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date         TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(16),
    image               VARCHAR(64)
);

-- lang --

CREATE TABLE IF NOT EXISTS ref_lang (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date         TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(16),
    alias               VARCHAR(3)
);

-- currency --

CREATE TABLE IF NOT EXISTS ref_currency (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date         TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(16),
    alias               VARCHAR(3),
    code                SMALLINT,
    rate                FLOAT DEFAULT 1
);

-- address --

CREATE TABLE IF NOT EXISTS ref_country (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS ref_city (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(32),
    country_id          INTEGER,
    FOREIGN KEY (country_id) REFERENCES ref_country(id)
);

CREATE TABLE IF NOT EXISTS ref_address (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    city_id             INTEGER,
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
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    firstname           VARCHAR(32),
    lastname            VARCHAR(32),
    phone               VARCHAR(15),
    email               VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS ref_customer_to_address (
    customer_id         INTEGER,
    address_id          INTEGER,
    FOREIGN KEY (customer_id) REFERENCES ref_customer(id),
    FOREIGN KEY (address_id) REFERENCES ref_address(id),
    PRIMARY KEY (customer_id, address_id)
);

-- company --

CREATE TABLE IF NOT EXISTS ref_company (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(32),
    address_id          INTEGER,
    FOREIGN KEY (address_id) REFERENCES ref_address(id)
);

CREATE TABLE IF NOT EXISTS ref_store (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    title               VARCHAR(32),
    company_id          INTEGER,
    address_id          INTEGER,
    FOREIGN KEY (company_id) REFERENCES ref_company(id),
    FOREIGN KEY (address_id) REFERENCES ref_address(id)
);

-- category0 --

CREATE TABLE IF NOT EXISTS ref_category0 (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    parent_id           INTEGER,
    image               VARCHAR(64),
    sort_order          SMALLINT
);

CREATE TABLE IF NOT EXISTS ref_category0_lang (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_id         INTEGER,
    lang_id             INTEGER,
    title               VARCHAR(128),
    descr               TEXT,
    FOREIGN KEY (category_id) REFERENCES ref_category0(id),
    FOREIGN KEY (lang_id) REFERENCES ref_lang(id)
);

-- product0 --

CREATE TABLE IF NOT EXISTS ref_product0 (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date         TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    model               VARCHAR(16)
);

CREATE TABLE IF NOT EXISTS ref_product0_image (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date         TIMESTAMP,
    image               VARCHAR(64),
    sort_order          SMALLINT,
    product_id          INTEGER,
    FOREIGN KEY (product_id) REFERENCES ref_product0(id)
);

CREATE TABLE IF NOT EXISTS ref_product0_lang (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date         TIMESTAMP,
    title               VARCHAR(128),
    descr               TEXT,
    product_id          INTEGER,
    lang_id             INTEGER,
    FOREIGN KEY (product_id) REFERENCES ref_product0(id),
    FOREIGN KEY (lang_id) REFERENCES ref_lang(id)
);

CREATE TABLE IF NOT EXISTS ref_product0_to_category (
    product_id          INTEGER,
    category_id         INTEGER,
    FOREIGN KEY (product_id) REFERENCES ref_product0(id),
    FOREIGN KEY (category_id) REFERENCES ref_category0(id),
    PRIMARY KEY (product_id, category_id)
);

-----------
-- store --
-----------

-- price --

CREATE TABLE IF NOT EXISTS ref_price (
    id                  SERIAL PRIMARY KEY,
    title               VARCHAR(16),
    currency_id         INTEGER,
    store_id            INTEGER,
    FOREIGN KEY (currency_id) REFERENCES ref_currency(id),
    FOREIGN KEY (store_id) REFERENCES ref_store(id)
);

-- category --

CREATE TABLE IF NOT EXISTS ref_category (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    parent_id           INTEGER,
    image               VARCHAR(64),
    sort_order          SMALLINT
);

CREATE TABLE IF NOT EXISTS ref_category_lang (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_id         INTEGER,
    lang_id             INTEGER,
    title               VARCHAR(128),
    descr               TEXT,
    FOREIGN KEY (category_id) REFERENCES ref_category(id),
    FOREIGN KEY (lang_id) REFERENCES ref_lang(id)
);

-- product --

CREATE TABLE IF NOT EXISTS ref_product (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date         TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    model               VARCHAR(16),
    code                VARCHAR(10),
    is_service          BOOLEAN DEFAULT FALSE,
    product0_id         INTEGER,
    store_id            INTEGER NOT NULL,
    FOREIGN KEY (product0_id) REFERENCES ref_product0(id),
    FOREIGN KEY (store_id) REFERENCES ref_store(id),
    UNIQUE (store_id, code)
);

CREATE TABLE IF NOT EXISTS ref_product_price (
    id                  SERIAL PRIMARY KEY,
    product_id          INTEGER,
    price_id            INTEGER,
    price               FLOAT DEFAULT 0,
    amount              INTEGER DEFAULT 1,
    FOREIGN KEY (product_id) REFERENCES ref_product(id),
    FOREIGN KEY (price_id) REFERENCES ref_price(id)
);

CREATE TABLE IF NOT EXISTS ref_product_price_history (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    product_price_id    INTEGER,
    price               FLOAT DEFAULT 0,
    FOREIGN KEY (product_price_id) REFERENCES ref_product_price(id)
);

CREATE TABLE IF NOT EXISTS ref_product_barcode (
    id                  SERIAL PRIMARY KEY,
    code                VARCHAR(13),
    ident				product_ident,
    product_id          INTEGER NOT NULL,
    store_id            INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES ref_product(id),
    FOREIGN KEY (store_id) REFERENCES ref_store(id),
    UNIQUE (store_id, code)
);

CREATE TABLE IF NOT EXISTS ref_product_image (
    id                  SERIAL PRIMARY KEY,
    image               VARCHAR(64),
    sort_order          SMALLINT,
    product_id          INTEGER,
    FOREIGN KEY (product_id) REFERENCES ref_product(id)
);

CREATE TABLE IF NOT EXISTS ref_product_lang (
    title               VARCHAR(128),
    descr               TEXT,
    product_id          INTEGER,
    lang_id             INTEGER,
    FOREIGN KEY (product_id) REFERENCES ref_product(id),
    FOREIGN KEY (lang_id) REFERENCES ref_lang(id),
    PRIMARY KEY (product_id, lang_id)
);

CREATE TABLE IF NOT EXISTS ref_product_to_category (
    product_id          INTEGER,
    category_id         INTEGER,
    store_id            INTEGER,
    FOREIGN KEY (product_id) REFERENCES ref_product(id),
    FOREIGN KEY (category_id) REFERENCES ref_category(id),
    FOREIGN KEY (store_id) REFERENCES ref_store(id),
    PRIMARY KEY (product_id, category_id, store_id)
);
