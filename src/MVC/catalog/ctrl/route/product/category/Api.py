# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from IncP.LibCtrl import TDbSql, GetDictDef


async def Main(self, aData: dict = None) -> dict:
    aPath, aTenantId, aLangId, aPage, aLimit = GetDictDef(
        aData.get('query'),
        ('path', 'tenant', 'lang', 'page', 'limit'),
        ('0', 2, 1, 0, 15), True
    )

    CategoriyIds = aPath.split('_')
    ResCategory = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_CategoriesSubCount_TenantParentLang',
            'param': {'aTenantId': aTenantId, 'aLangId': aLangId, 'aParentIdtRoot': 0, 'aParentIdts': CategoriyIds},
            'query': True
        }
    )

    DblData = ResCategory.get('data')
    if (DblData):
        Deep = len(CategoriyIds)
        Dbl = TDbSql().Import(DblData)
        DblOut = Dbl.New()
        DblOut.AddFields(['href'])

        Products = 0
        for Rec in Dbl:
            if (Deep == Rec.deep):
                Products += Rec.products
                Data = Rec.GetAsList() + (f'?route=product/category&path={aPath}_{Rec.idt}',)
                DblOut.RecAdd(Data)

        if (DblOut.GetSize() > 0):
            ResCategory['dbl_category'] = DblOut.Export()
            CategoryIds = DblOut.ExportList('id')
        else:
            Dbl.RecNo = 0
            RecNo = Dbl.FindField('idt', int(CategoriyIds[-1]))
            if (RecNo != -1):
                Rec = Dbl.RecGo(RecNo)
                CategoryIds = [Rec.id]
                Products = Rec.products

        PageCount = Products // aLimit
        #Pages = [f'route=product/category&path={aPath}&page={i+1}' for i in range(PageCount)]
        #DblPage = TDbSql(['page'], [Pages])
        #ResCategory['dbl_pages'] = DblPage.Export()
        ResCategory['pages'] = list(range(1, PageCount + 1))

        Offset = aPage * aLimit
        ResProduct = await self.ExecModel(
            'ref_product/category',
            {
                'method': 'Get_CategoriesProducts_LangImagePrice',
                'param': {'aCategoryIds': CategoryIds, 'aLangId': aLangId, 'aPriceId': 3, 'aLimit': aLimit, 'aOffset': Offset}
            }
        )
        ResCategory['dbl_product'] = ResProduct.get('data')
    return ResCategory
