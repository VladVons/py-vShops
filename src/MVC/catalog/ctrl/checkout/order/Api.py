# Created: 2024.03.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    aLang, aOrderId, aCRC = Lib.GetDictDefs(
        aData.get('query'),
        ('lang', 'order_id', 'crc'),
        ('ua', 0, 0)
    )
    aLangId = self.GetLangId(aLang)

    if (not Lib.IsDigits([aOrderId, aCRC])) or (Lib.GetCRC(str(aOrderId)) != aCRC):
        return {'status_code': 404}


    DblOrder = await self.ExecModelImport(
        'doc_sale',
        {
            'method': 'Get_OrderMix',
            'param': {'aOrderId': aOrderId}
        }
    )

    if (not DblOrder):
        return {'status_code': 404}

    DblOrderProducts = await self.ExecModelImport(
        'doc_sale',
        {
            'method': 'Get_OrderMixTableProduct',
            'param': {
                'aOrderId': aOrderId,
                'aLangId': aLangId
            }
        }
    )

    DblOrderProducts.AddFieldsFill(['href'], False)
    for Rec in DblOrderProducts:
        New = [f'/?route=product0/product&product_id={Rec.id}']
        DblOrderProducts.RecMerge(New)

    return {
        'order': DblOrder.Rec.GetAsDict(),
        'dbl_order_products': DblOrderProducts.Export()
        }
