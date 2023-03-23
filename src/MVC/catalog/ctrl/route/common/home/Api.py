# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbSql


async def Main(self, aData: dict = None) -> dict:
    Res = {}

    await self.Lang.Add(aData['module'])
    await self.Lang.Add('route/misc/about')
    #Text = self.Lang.Get('service')
    #Res['lang'] = self.Lang
    Res['lang'] = self.Lang.Join()

    CategoryId = aData['query'].get('category', 0)
    TenantId = aData['query'].get('tenant', 2)
    LangId = aData['query'].get('lang', 1)

    Data = await self.ExecModel(
        'ref_product/category',
        {
            "method": "Get_Categories_TenantParentLang",
            "param": {'aTenantId': TenantId, 'aParentIdt': CategoryId, 'aLangId': LangId, 'aDepth': 1}
        }
    )

    Res['category'] = Data.get('data')
    #Dbl = TDbSql().Import(Res['category'])
    #Ids = Dbl.ExportListComma('id')

    if (Data['info']['status'] != 200):
        return {'err': Data.get('err')}

    return Res
