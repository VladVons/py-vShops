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
            'method': 'Get_CategoriesSubCount_TenantParentLang',
            'param': {'aTenantId': aTenantId, 'aLangId': aLangId, 'aParentIdtRoot': 0, 'aParentIdts': CategoriyIds},
            'query': True
        }
    )

    DblData = Res.get('data')
    if (DblData):
        Deep = len(CategoriyIds)
        Dbl = TDbSql().Import(DblData)
        DblOut = Dbl.New()
        DblOut.AddFields(['href'])
        for Rec in Dbl:
            if (Deep == Rec.deep):
                Data = Rec.GetAsList() + (f'?route=product/category&path={aPath}_{Rec.idt}',)
                DblOut.RecAdd(Data)
        if (DblOut.GetSize() > 0):
            Res['dbl_category'] = DblOut.Export()
            CategoriesComma = DblOut.ExportListComma('id')
        else:
            Dbl.RecNo = 0
            RecNo = Dbl.FindField('idt', int(CategoriyIds[-1]))
            if (RecNo != -1):
                CategoriesComma = Dbl.RecGo(RecNo).GetField('id')
    return Res
