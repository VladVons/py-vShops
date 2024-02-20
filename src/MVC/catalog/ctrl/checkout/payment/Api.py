# Created: 2024.02.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


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
    Post = aData.get('post')
    if (Post):
        pass

    Res = {
        'href': {
            'novaposhta_ajax': '/api/?route=checkout/payment'
        }
    }
    return Res
