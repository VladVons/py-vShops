# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.UtilP.Db.ADb import ListIntToComma


def GetProductsLang(aProductId: list[int], aLangId: id) -> str:
    return f'''
    select
		rpl.product_id,
   		rpl.title,
        rpl.descr,
        rpl.feature
    from
        ref_product_lang rpl
    where
        (rpl.product_id in ({ListIntToComma(aProductId)})) and
        (rpl.lang_id = {aLangId})
    '''

def GetProductsWithoutLang(aTenantId: int, aLangId: int) -> str:
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

