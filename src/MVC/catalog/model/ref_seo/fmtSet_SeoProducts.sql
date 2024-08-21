--fmtSet_SeoProducts.sql

insert into
    ref_seo_url (attr, val, keyword, sort_order)
(
    select
        'tenant_id' as attr,
        id as val,
        cyrtolat_url(title) as title,
        0 as sort_order
    from
        ref_tenant rt
    where
        (rt.enabled) and 
        (rt.id > 0)

    union all

    select
        'category_id',
        id,
        cyrtolat_url(title),
        0
    from
        ref_product0_category rpc
    join
        ref_product0_category_lang rpcl on
        (rpcl.category_id = rpc.id) and (rpcl.lang_id = 1)
    where
        (rpc.enabled) and
        (rpc.parent_id is not null)

    union all

    select
        'product_id',
        id,
        cyrtolat_url(title) || '_t' || tenant_id,
        0
    from
        ref_product rp
    join
        ref_product_lang rpl on
        (rpl.product_id = rp.id) and (rpl.lang_id = 1)
    where
        (rp.enabled)
)
on conflict
    (attr, val)
do update set
    keyword = excluded.keyword;
