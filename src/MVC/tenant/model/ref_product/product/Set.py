# Created: 2023.12.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from IncP.LibModel import DTransaction, TDbExecCursor, TDbSql, DictToComma, ListToComma


async def Del_TenantImages(self, aTenantId: int, aImages: list[str]):
    Arr = [f"image like '{x}'" for x in aImages]
    CondLike = ' or '.join(Arr)
    return await self.ExecQuery(
        'fmtDel_TenantImages.sql',
        {'aTenantId': aTenantId, 'CondLike': CondLike}
    )

async def Upd_TenantImages(self, aProductId: int, aTenantId: int, aImages: list[str]) -> str:
    Arr = [f"({aProductId}, '{xImage}'" for xImage in aImages]
    Data = ', '.join(Arr)
    return await self.ExecQuery(
        'fmtUpd_TenantImages.sql',
        {'aTenantId': aTenantId, 'Data': Data}
    )

def GetUpd_ProductToCategory(aCategoryId: list, aProductId):
    return f'''
        update ref_product_to_category
        set category_id = {aCategoryId}
        where (product_id = {aProductId})
    '''

def GetUpd_ProductLang(aData: dict, aProductId: int, aLangId: int) -> str:
    Values = DictToComma(aData)
    if (Values):
        return f'''
            update ref_product_lang
            set {Values}
            where (product_id = {aProductId}) and (lang_id = {aLangId})
        '''

def GetUpd_ProducPrice(aData: list) -> str:
    return f'''
        with src (product_id, price_id, price) as (
            values {', '.join(aData)}
        )
        merge into ref_product_price as dst
        using src
        on (dst.product_id = src.product_id) and (dst.price_id = src.price_id) and (dst.qty = 1)
        when matched and (manual is null or manual = false) then
            update set price = src.price
        when not matched then
            insert (product_id, price_id, price)
            values (src.product_id, src.price_id, src.price)
    '''

def GetUpd_Product(aData: dict, aProductId: int) -> str:
    Values = DictToComma(aData)

    return f'''
        update ref_product
        set {Values}
        where (id = {aProductId})
    '''

@DTransaction
async def _Set_Product(self, aData: dict, aCursor = None) -> dict:
    aTenantId = aData['aTenantId']
    aProductId = aData['aProductId']
    aPost = aData['aPost']
    Changes = json.loads(aPost['changes'])

    DblData = await self.ApiModel.Exec(
        'system',
        {
            'method': 'Get_TenantInf',
            'param': {'aTenantId': aTenantId}
        })
    DblTenant = TDbSql().Import(DblData['data'])

    if ('quantity' in Changes):
        Query = f'''
            select stock_set_tenant(
                {aProductId},
                {Changes['quantity'][1]},
                {aTenantId}
            )
        '''
        await TDbExecCursor(aCursor).Exec(Query)

    # ref_product_price
    Values = []
    if ('price_sale' in Changes):
        Value = f'({aProductId}, {DblTenant.Rec.price.get("sale")}, {Changes["price_sale"][1]})'
        Values.append(Value)

    if ('price_purchase' in Changes):
        Value = f'({aProductId}, {DblTenant.Rec.price.get("purchase")}, {Changes["price_purchase"][1]})'
        Values.append(Value)

    if (Values):
        Query = GetUpd_ProducPrice(Values)
        await TDbExecCursor(aCursor).Exec(Query)

    # ref_product
    Values = {}
    if ('enabled' in Changes):
        Values['enabled'] = Changes['enabled'][1]

        Query = GetUpd_Product(Values, aProductId)
        if (Query):
            await TDbExecCursor(aCursor).Exec(Query)

    # ref_product_to_category
    if ('category_id' in Changes):
        Query = GetUpd_ProductToCategory(Changes['category_id'][1], aProductId)
        await TDbExecCursor(aCursor).Exec(Query)

    # ref_product_lang
    Values = {}
    if ('title' in Changes):
        Values['title'] = Changes['title'][1]

    if ('descr' in Changes):
        Values['descr'] = Changes['descr'][1]

    Query = GetUpd_ProductLang(Values, aProductId, 1)
    if (Query):
        await TDbExecCursor(aCursor).Exec(Query)


async def Set_Product(self, aLangId: int, aTenantId: int, aProductId: int, aPost: dict) -> dict:
    await _Set_Product(self, locals())
