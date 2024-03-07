# Created: 2024.02.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbList


async def ajax(self, aData: dict = None) -> dict:
    Res = {}
    match aData['input_name']:
        case 'town':
            Data = await self.NovaPoshta.SearchtAddress(aData['input_value'])
            if (Data):
                Arr = Data['data'][0]['Addresses']
                Res['items'] = [{'present': x['Present'], 'ref': x['MainDescription']} for x in Arr]
        case 'department':
            Data = await self.NovaPoshta.Warehouses(aData['input_value'], aData['town_ref'])
            if (Data):
                Arr = Data['data']
                Res['items'] = [{'present': x['Description'], 'ref': x['Ref']} for x in Arr]
    return Res

async def Main(self, aData: dict = None) -> dict:
    OrderId = None
    Post = aData.get('post')
    if (Post):
        DblCastomer = await self.ExecModelImport(
            'ref_person',
            {
                'method': 'Set_PersonPhoneName',
                'param': {
                    'aPhone': Post['phone'],
                    'aFirstName': Post['first_name'],
                    'aLastName': Post['last_name'],
                    'aMiddleName': Post['middle_name']
                }
            }
        )

        DblProducts = TDbList().LoadStr(Post['cart'])
        DblOrderMix = await self.ExecModelImport(
            'doc_sale',
            {
                'method': 'Add_OrderMix',
                'param': {
                    'aCustomerId': DblCastomer.Rec.id,
                    'aRows': DblProducts.ExportData(['id', 'qty', 'price'])
                }
            }
        )
        OrderId = DblOrderMix.Rec.id

    return {
        'href': {
            'novaposhta_ajax': '/api/?route=checkout/payment',
            'order_id': OrderId
        }
    }
