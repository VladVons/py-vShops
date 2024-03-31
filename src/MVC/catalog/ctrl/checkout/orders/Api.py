# Created: 2023.09.09
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    aLang, aCustomerId, aCRC = Lib.GetDictDefs(
        aData.get('query'),
        ('lang', 'customer_id', 'crc'),
        ('ua', 0, 0)
    )

    if (not Lib.IsDigits([aCustomerId, aCRC])) or (Lib.GetCRC(str(aCustomerId)) != aCRC):
        return {'status_code': 404}

    if (not aCustomerId):
        return {
            'status_code': 301,
            'status_value': '/?route=checkout/xxx'
        }

    DblOrders = await self.ExecModelImport(
        'doc_sale',
        {
            'method': 'Get_OrdersMix',
            'param': {'aCustomerId': aCustomerId}
        }
    )

    if (DblOrders):
        DblOrders.ToList().AddFields(['href'])
        for Rec in  DblOrders:
            Href = f'/?route=checkout/history&order_id={Rec.order_id}'
            Rec.SetField('href', Href)

        return {'dbl_orders': DblOrders.Export()}
