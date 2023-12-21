# Created: 2023.12.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


#from Inc.DictDef import TDictDef
from IncP.LibModel import DTransaction, TDbExecCursor, TDbSql, DictToComma


def Get_Upd_Product(aData: dict, aProductId: int) -> str:
    Values = DictToComma(aData)
    if (Values):
        return f'''
            update ref_product
            set {Values}
            where (id = {aProductId})
        '''

def Get_Upd_ProductLang(aData: dict, aProductId: int, aLangId: int) -> str:
    Values = DictToComma(aData)
    if (Values):
        return f'''
            update ref_product_lang
            set {Values}
            where (product_id = {aProductId}) and (lang_id = {aLangId})
        '''

@DTransaction
async def _Set_Product(self, aData: dict, aCursor = None) -> dict:
    aTenantId = aData['aTenantId']
    aProductId = aData['aProductId']
    Changes = aData['aChanges']

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
                {Changes['quantity']},
                {aTenantId}
            )
        '''
        await TDbExecCursor(aCursor).Exec(Query)

    # ref_product_price
    Values = []
    if ('price_sale' in Changes):
        Value = f'({aProductId}, {DblTenant.Rec.price.get("sale")}, {Changes["price_sale"]})'
        Values.append(Value)

    if ('price_purchase' in Changes):
        Value = f'({aProductId}, {DblTenant.Rec.price.get("purchase")}, {Changes["price_purchase"]})'
        Values.append(Value)

    if (Values):
        Query = f'''
            with src (product_id, price_id, price) as (
                values {', '.join(Values)}
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
        await TDbExecCursor(aCursor).Exec(Query)

    # ref_product
    Values = {}
    if ('enabled' in Changes):
        Values['enabled'] = Changes['enabled']

    Query = Get_Upd_Product(Values, aProductId)
    if (Query):
        await TDbExecCursor(aCursor).Exec(Query)

    # ref_product_lang
    Values = {}
    if ('title' in Changes):
        Values['title'] = Changes['title']

    if ('descr' in Changes):
        Values['descr'] = Changes['descr']

    Query = Get_Upd_ProductLang(Values, aProductId, 1)
    if (Query):
        await TDbExecCursor(aCursor).Exec(Query)

    pass


async def Set_Product(self, aLangId: int, aTenantId: int, aProductId: int, aChanges: dict) -> dict:
    await _Set_Product(self, locals())
