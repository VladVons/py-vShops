# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import ListIntToComma


def GetProducts(aProductId: list[int]) -> str:
    ProductsId = ListIntToComma(aProductId)

    return f'''
    select
        rp.id,
        rp.enabled,
        rp.model,
        rp.is_service,
        rp.idt,
        rp.product0_id
    from
        ref_product rp
    where
        (rp.id in ({ProductsId}))
    '''

def GetProductsByIdt(aProductIdt: list[int]) -> str:
    ProductsIdt = ListIntToComma(aProductIdt)

    return f'''
    select
        rp.id,
        rp.enabled,
        rp.model,
        rp.is_service,
        rp.idt,
        rp.product0_id
    from
        ref_product rp
    where
        (rp.idt in ({ProductsIdt}))
    '''
