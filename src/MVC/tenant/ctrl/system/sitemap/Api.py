# Created: 2024.02.09
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def ajax(self, aData: dict) -> dict:
    Param = aData.get('param', {})
    match Param['method']:
        case 'get_count':
            Dbl = await self.ExecModelImport(
                'system',
                {
                    'method': 'Get_Seo_ProductsCount'
                }
            )
            return Dbl.Rec.GetAsDict()

        case 'get_data':
            Dbl = await self.ExecModelImport(
                'system',
                {
                    'method': 'Get_Seo_Products',
                    'param': {
                        'aLimit': Param['limit'],
                        'aOffset': Param['offset']
                    }
                }
            )
            return Dbl.Export()

async def Main(self, aData: dict) -> dict:
    pass