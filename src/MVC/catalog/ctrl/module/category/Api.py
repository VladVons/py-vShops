# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDef, TDbSql


async def Main(self, aData: dict = None) -> dict:
    aPath, aTenantId, aLangId = GetDictDef(
        aData.get('query'),
        ('path', 'tenant', 'lang'),
        ('0', 1, 1)
    )

    CategoriyIds = aPath.split('_')
    Res = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_Categories_TenantParentLang',
            'param': {'aTenantId': aTenantId, 'aLangId': aLangId, 'aParentIdtRoot': 0, 'aParentIdts': CategoriyIds[:2]}
        }
    )

    DblData = Res.get('data')
    if (DblData):
        Href = []
        Dbl = TDbSql().Import(DblData)
        for Rec in Dbl:
            if (Rec.parent_idt):
                Path = '_'.join(CategoriyIds[:2])
                if (len(CategoriyIds) > 2):
                    Res['category_id'] = int(CategoriyIds[-1])
            else:
                Path = '0'
            Href.append(f'?route=product/category&path={Path}_{Rec.idt}')
        Dbl.AddFields(['href'], [Href])
        Res['data'] = Dbl.Export()
    return Res
