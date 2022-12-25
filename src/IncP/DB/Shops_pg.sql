-- Created: 2022.12.25
-- Author: Vladimir Vons <VladVons@gmail.com>
-- License: GNU, see LICENSE for more details


CREATE TABLE IF NOT EXISTS country (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    name                VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS city (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    name                VARCHAR(32),
    country_id          INTEGER,
    FOREIGN KEY (country_id) REFERENCES country(id)
);

CREATE TABLE IF NOT EXISTS address (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    city_id             INTEGER,
    post_code           VARCHAR(8),
    street              VARCHAR(32),
    house               VARCHAR(4),
    room                VARCHAR(4),
    door_code           VARCHAR(8),
    FOREIGN KEY (city_id) REFERENCES city(id)
);

CREATE TABLE IF NOT EXISTS customer (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    firstname           VARCHAR(32),
    lastname            VARCHAR(32),
    phone               VARCHAR(15),
    email               VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS customer_to_address (
    customer_id         INTEGER,
    address_id          INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (address_id) REFERENCES address(id)
);

CREATE TABLE IF NOT EXISTS company (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    name                VARCHAR(32),
    address_id          INTEGER,
    FOREIGN KEY (address_id) REFERENCES address(id)
);

CREATE TABLE IF NOT EXISTS store (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    name                VARCHAR(32),
    company_id          INTEGER,
    address_id          INTEGER,
    FOREIGN KEY (company_id) REFERENCES company(id),
    FOREIGN KEY (address_id) REFERENCES address(id)
);

CREATE TABLE IF NOT EXISTS category (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE,
    parent_id           INTEGER,
    image               VARCHAR(128),
    sort_order          SMALLINT
);

CREATE TABLE IF NOT EXISTS category_description (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_id         INTEGER,
    language_id         INTEGER,
    name                VARCHAR(128),
    description         TEXT,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (language_id) REFERENCES language(id)
);

CREATE TABLE IF NOT EXISTS product (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled             BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS product_image (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image               VARCHAR(128),
    sort_order          SMALLINT,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE IF NOT EXISTS product_description (
    id                  SERIAL PRIMARY KEY,
    create_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    product_id          INTEGER,
    language_id         INTEGER,
    name                VARCHAR(128),
    description         TEXT,
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (language_id) REFERENCES language(id)
);

CREATE TABLE IF NOT EXISTS product_to_category (
    product_id          INTEGER,
    category_id         INTEGER,
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
);
