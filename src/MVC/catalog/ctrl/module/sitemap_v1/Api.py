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
        DblPages.ToList()
        for Rec in DblPages:
            Rec.route = f'/?route={Rec.route}'

    return {
        'categories_a': Categories, 'id_a': 0,
        'dbl_pages': DblPages.Export()
    }
