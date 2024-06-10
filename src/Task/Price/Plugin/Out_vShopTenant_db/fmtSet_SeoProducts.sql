--fmtSet_SeoProducts.sql
-- aLangId, aTenantId

insert into
    ref_seo_url (attr, val, keyword, sort_order)
(
    select
        'tenant_id' as attr,
        rt.id as val,
        lower(cyrtolat(rt.title)) as title,
        0 as sort_order
    from
        ref_tenant rt
    where
        (rt.enabled) and
        (rt.id = {aTenantId})

    union all

    select
        'category_id',
        rpc.id,
        translate(lower(cyrtolat(rpcl.title)), ' /.&=', '___'),
        0
    from
        ref_product0_category rpc
    join
        ref_product0_category_lang rpcl on
        (rpcl.category_id = rpc.id) and (rpcl.lang_id = {aLangId})
    where
        (rpc.enabled) and
        (rpc.parent_id is not null)

    union all

    select
        'product_id',
        rp.id,
        translate(lower(cyrtolat(rpl.title)), ' /.&=', '___') || '_t' || rp.tenant_id,
        0
    from
        ref_product rp
    join
        ref_product_lang rpl on
        (rpl.product_id = rp.id) and (rpl.lang_id = {aLangId})
    where
        (rp.enabled) and
        (rp.tenant_id = {aTenantId})
)
on conflict
    (attr, val)
do update set
    keyword = excluded.keyword
