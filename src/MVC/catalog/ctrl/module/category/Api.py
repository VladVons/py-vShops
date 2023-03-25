# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDef, TDbSql


async def Main(self, aData: dict = None) -> dict:
    aCategoryId, aTenantId, aLangId = GetDictDef(aData.get('query'), ('category', 'tenant', 'lang'), (0, 2, 1))
    Res = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_Categories_TenantParentLang',
            "param": {'aTenantId': aTenantId, 'aParentIdt': aCategoryId, 'aLangId': aLangId, 'aDepth': 1}
        }
    )

    Href = []
    Dbl = TDbSql().Import(Res.get('data'))
    for Rec in Dbl:
        Href.append(f'product/category&path={Rec.idt}')
    Dbl.AddFields(['href'], [Href])
    Res['data'] = Dbl.Export()
    return Res
