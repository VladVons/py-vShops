# Created: 2023.09.09
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs


async def Main(self, aData: dict = None) -> dict:
    aCustomerId, = GetDictDefs(
        aData.get('query'),
        ('customer_id', ),
        ('', )
    )

    if (not aCustomerId):
        return {
            'status_code': 301,
            'status_value': '/?route=checkout/xxx'
        }

    DblOrdersMix = await self.ExecModelImport(
        'doc_sale',
        {
            'method': 'Get_OrdersMix',
            'param': {'aCustomerId': aCustomerId}
        }
    )

    if (DblOrdersMix):
        DblOrdersMix.ToList().AddFields(['href'])
        for Rec in  DblOrdersMix:
            Href = f'/?route=checkout/history&order_id={Rec.order_id}'
            Rec.SetField('href', Href)

        return {'dbl_orders': DblOrdersMix.Export()}
