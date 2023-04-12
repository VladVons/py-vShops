# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from IncP.LibCtrl import TDbSql, GetDictDef


async def Main(self, aData: dict = None) -> dict:
    aPath, aTenantId, aLangId = GetDictDef(aData.get('query'), ('path', 'tenant', 'lang'), ('0', '2', '1'))
    CategoriyIds = aPath.split('_')
    Res = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_Categories_TenantParentLang',
            'param': {'aTenantId': aTenantId, 'aLangId': aLangId, 'aParentIdts': [CategoriyIds[-1]], 'aDepth': 1},
            'query': False
        }
    )

    DblData = Res.get('data')
    if (DblData):
        Href = []
        Dbl = TDbSql().Import(DblData)
        for Rec in Dbl:
            Href.append(f'?route=product/category&path={aPath}_{Rec.idt}')
        Dbl.AddFields(['href'], [Href])
        Res['dbl_category'] = Dbl.Export()

        CategoriesComma = Dbl.ExportListComma('id')
        return Res
