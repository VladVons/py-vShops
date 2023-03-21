INSERT INTO public.ref_country (id, enabled, deleted, title) VALUES (1, true, false, 'country 1');
INSERT INTO public.ref_country (id, enabled, deleted, title) VALUES (2, true, false, 'country 2');

INSERT INTO public.ref_city (id, enabled, deleted, title, country_id) VALUES (1, true, false, 'city 1', 1);
INSERT INTO public.ref_city (id, enabled, deleted, title, country_id) VALUES (2, true, false, 'city 2', 2);

INSERT INTO public.ref_address (id, enabled, deleted, city_id, post_code, street, house, room, door_code) VALUES (1, true, false, 1, NULL, 'street 1', '1a', NULL, NULL);
INSERT INTO public.ref_address (id, enabled, deleted, city_id, post_code, street, house, room, door_code) VALUES (2, true, false, 2, NULL, 'street 2', '2a', NULL, NULL);

INSERT INTO public.ref_currency (id, enabled, deleted, title, alias, code, rate) VALUES (1, true, false, 'currency 1', 'uah', NULL, 1);
INSERT INTO public.ref_currency (id, enabled, deleted, title, alias, code, rate) VALUES (2, true, false, 'currency 2', 'pln', NULL, 1);

INSERT INTO public.ref_tenant (id, enabled, deleted, title, address_id) VALUES (1, true, false, 'company 1', 1);
INSERT INTO public.ref_tenant (id, enabled, deleted, title, address_id) VALUES (2, true, false, 'company 2', 2);

INSERT INTO public.ref_lang (id, enabled, deleted, title, alias) VALUES (1, true, false, 'lang 1', 'ua');

INSERT INTO public.ref_price (id, title, currency_id, tenant_id, idt) VALUES (1, 'price 1', 1, 1, 1);
INSERT INTO public.ref_price (id, title, currency_id, tenant_id, idt) VALUES (2, 'price 2', 1, 1, 2);
INSERT INTO public.ref_price (id, title, currency_id, tenant_id, idt) VALUES (3, 'price 1', 1, 2, 1);
INSERT INTO public.ref_price (id, title, currency_id, tenant_id, idt) VALUES (4, 'price 2', 1, 2, 2);
