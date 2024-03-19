# Created: 2024.02.12
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import DeepGetByList
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
        DblNew = DblPages.New()
        for Rec in DblPages:
            if (Rec.route not in ['product0/category', 'common/home', 'info/sitemap']):
                RecNew = DblNew.RecAdd()
                RecNew.route = f'/?route={Rec.route}'
                RecNew.title = Rec.title
        DblPages = DblNew

    return {
        'categories_a': Categories, 'id_a': 0,
        'dbl_pages': DblPages.Export()
    }
