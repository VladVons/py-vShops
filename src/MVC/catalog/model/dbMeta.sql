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
    when (old.* is distinct from new.*)
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
