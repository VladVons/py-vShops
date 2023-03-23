# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbSql


async def Main(self, aData: dict = None) -> dict:
    Res = {}

    aCategoryId = aData['query'].get('category', 0)
    aTenantId = aData['query'].get('tenant', 2)
    aLangId = aData['query'].get('lang', 1)
    aRoute = aData['route']

    Data = await self.ExecModel(
        'system',
        {
            'method': 'Get_Module_RouteLang',
            'param': {'aRoute': aRoute, 'aLangId': aLangId}
        }
    )

    Modules = Data.get('data')
    if (Modules):
        Dbl = TDbSql().Import(Modules)
        for Rec in Dbl:
            Module = Rec.GetField('code')
            Data = await self.ExecSelf(f'module/{Module}', {})

    await self.Lang.Add(aData['module'])
    await self.Lang.Add('route/misc/about')
    #Text = self.Lang.Get('service')
    #Res['lang'] = self.Lang
    Res['lang'] = self.Lang.Join()

    Data = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_Categories_TenantParentLang',
            "param": {'aTenantId': aTenantId, 'aParentIdt': aCategoryId, 'aLangId': aLangId, 'aDepth': 1}
        }
    )

    Res['category'] = Data.get('data')
    #Dbl = TDbSql().Import(Res['category'])
    #Ids = Dbl.ExportListComma('id')

    if (Data['info']['status'] != 200):
        return {'err': Data.get('err')}

    return Res
