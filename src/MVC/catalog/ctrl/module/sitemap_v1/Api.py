# Created: 2024.02.12
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib
from ..._inc.layout1.Api import GetCategories

async def Main(self, aData: dict = None) -> dict:
    aLang = Lib.DeepGetByList(aData, ['query', 'lang'], 'ua')
    LangId = self.GetLangId(aLang)
    Categories = await GetCategories(self, LangId)

    DblPages = await self.ExecModelImport(
        'system',
        {
            'method': 'Get_LayoutRoute',
            'param': {}
        }
    )
    if (DblPages):
        Hrefs = [f'/?route={Rec.route}' for Rec in DblPages]
        if (self.ApiCtrl.Conf.get('seo_url')):
            Hrefs = await Lib.SeoEncodeList(self, Hrefs)

        DblPages.AddFields(['href'], [Hrefs])

    return {
        'categories_a': Categories, 'id_a': 0,
        'dbl_pages': DblPages.Export()
    }
