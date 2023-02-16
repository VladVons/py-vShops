# 0.50
def GetProductsWithoutLang(aTenantId: int, aLangId: int) -> str:
    return f'''
    select
        rp.id
    from
        ref_product rp
    where
        rp.id not in (
            select
                rpl.product_id
            from
                ref_product_lang rpl
            left join
                ref_product rp on
                (rpl.product_id = rp.id)
            where
                (rpl.lang_id = {aLangId}) and
                (rp.tenant_id = {aTenantId})
        )
    order by
        rp.id
    '''

# 0.45
def GetProductsWithoutLang2(aTenantId: int, aLangId: int) -> str:
    return f'''
    with wrpl as (
        select
            rpl.product_id
        from
            ref_product_lang rpl
        left join
            ref_product rp on
            (rpl.product_id = rp.id)
        where
            (rpl.lang_id = {aLangId}) and
            (rp.tenant_id = {aTenantId})
    )

    select
        rp.id
    from
        ref_product rp
    left join
        wrpl on
        rp.id = wrpl.product_id
    where
        (wrpl.product_id is null)
    order by
        rp.id
    '''
