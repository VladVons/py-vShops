# Created: 2024.02.09
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def ajax(self, aData: dict) -> dict:
    Param = aData.get('param', {})
    match Param['method']:
        case 'get_product_count':
            Dbl = await self.ExecModelImport(
                'system',
                {
                    'method': 'Get_Seo_ProductsCount'
                }
            )
            return Dbl.Rec.GetAsDict()

        case 'get_product_data':
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

        case 'get_categories_data':
            Dbl = await self.ExecModelImport(
                'system',
                {
                    'method': 'Get_Seo_Categories',
                    'param': {
                        'aLimit': Param['limit'],
                        'aOffset': Param['offset'],
                        'aLang': self.GetLangId('ua') # ToDo
                    }
                }
            )
            return Dbl.Export()

        case 'get_pages_data':
            Dbl = await self.ExecModelImport(
                'system',
                {
                    'method': 'Get_LayoutRoute',
                    'param': {
                        'aLimit': Param['limit'],
                        'aOffset': Param['offset']
                    }
                }
            )
            return Dbl.Export()

async def Main(self, aData: dict) -> dict:
    pass