# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import ListIntToComma


def GetProductsPrice(aProductId: list[int]) -> str:
    return f'''
    select
        rpp.product_id,
        rpp.price_id,
        rpp.price,
        rpp.qty
    from
        ref_product_price rpp
    where
        (rpp.product_id in ({ListIntToComma(aProductId)}))
    order by
        rpp.product_id,
        rpp.qty
    '''

def GetProductPriceOnDate(aProductId: int, aPriceId: int, aDate: str, aQty: int = 1) -> str:
    return f'''
    select
        rpph.price
    from
        ref_product_price_history rpph
    left join
        ref_product_price rpp on
        (rpph.price_id = rpp.id)
    where
        rpph.qty = {aQty} and
        rpph.create_date <= '{aDate}' and
        rpp.price_id = {aPriceId} and
        rpp.product_id = {aProductId}
    order by
        rpph.create_date desc
    limit
        1
    '''
