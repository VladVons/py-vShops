# Created: 2024.02.09
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib

async def AddHref(self, aDbl: Lib.TDbList, aHref: list[str]):
    if (aDbl):
        if (self.ApiCtrl.Conf.get('seo_url')):
            aHref = await Lib.SeoEncodeList(self, aHref)
        aDbl.AddFields(['href'], [aHref])

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
                    'method': 'Get_LimitProducts',
                    'param': {
                        'aLimit': Param['limit'],
                        'aOffset': Param['offset']
                    }
                }
            )

            Hrefs = [f'/?route=product0/product&product_id={Rec.id}' for Rec in Dbl]
            await AddHref(self, Dbl, Hrefs)
            return Dbl.Export()

        case 'get_categories_data':
            Dbl = await self.ExecModelImport(
                'system',
                {
                    'method': 'Get_LimitCategories',
                    'param': {
                        'aLimit': Param['limit'],
                        'aOffset': Param['offset'],
                        'aLang': self.GetLangId('ua') # ToDo
                    }
                }
            )

            Hrefs = [f'/?route=product0/category&category_id={Rec.id}' for Rec in Dbl]
            await AddHref(self, Dbl, Hrefs)
            return Dbl.Export()

        case 'get_pages_data':
            Dbl = await self.ExecModelImport(
                'system',
                {
                    'method': 'Get_LayoutRouteLimit',
                    'param': {
                        'aLimit': Param['limit'],
                        'aOffset': Param['offset']
                    }
                }
            )
            Hrefs = [f'/?route={Rec.route}' for Rec in Dbl]
            await AddHref(self, Dbl, Hrefs)
            return Dbl.Export()

async def Main(self, aData: dict) -> dict:
    pass
