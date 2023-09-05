# Created: 2023.04.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbList, GetDictDefs


async def ApiOrder(self, aData: dict = None) -> dict:
    aPhone, aFirstName, aProducts = GetDictDefs(
        aData,
        ('phone', 'client', 'cart'),
        ('', '', {})
    )

    DblCastomer = await self.ExecModelImport(
        'ref_customer',
        {
            'method': 'Set_CustomerPhoneName',
            'param': {'aPhone': aPhone, 'aFirstName': aFirstName}
        }
    )

    DblProducts = TDbList().Import(aProducts)
    DblOrderMix = await self.ExecModelImport(
        'doc_sale',
        {
            'method': 'Add_OrderMix',
            'param': {'aCustomerId': DblCastomer.Rec.id, 'aRows': DblProducts.Data}
        }
    )

    Res = {
        'status': 'ok',
        'order_id': DblOrderMix.Rec.id
    }
    return Res

async def Main(self, aData: dict = None) -> dict:
    Res = {}

    Res['href'] = {
        'confirm': '?route=checkout/confirm'
    }

    return Res
