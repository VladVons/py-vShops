# Created: 2024.02.12
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import DeepGetByList, SeoEncodeList
from ..._inc.layout1.Api import GetCategories

async def Main(self, aData: dict = None) -> dict:
    aLang = DeepGetByList(aData, ['query', 'lang'], 'ua')
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
            Hrefs = await SeoEncodeList(self, Hrefs)

        DblPages.ToList()
        for Idx, Rec in enumerate(DblPages):
            Rec.route = Hrefs[Idx]

    return {
        'categories_a': Categories, 'id_a': 0,
        'dbl_pages': DblPages.Export()
    }
