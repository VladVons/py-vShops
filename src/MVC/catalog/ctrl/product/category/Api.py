# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbSql, GetDictDef


async def Main(self, aData: dict = None) -> dict:
    aPath, aTenantId, aLangId, aPage, aLimit = GetDictDef(
        aData.get('query'),
        ('path', 'tenant', 'lang', 'page', 'limit'),
        ('0', 1, 1, 0, 15), True
    )

    CategoriyIds = list(map(int, aPath.split('_')))
    Res = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_CategoriesSubCount_TenantParentLang',
            'param': {'aTenantId': aTenantId, 'aLangId': aLangId, 'aParentIdtRoot': 0, 'aParentIdts': CategoriyIds},
            'query': False
        }
    )
    DblData = Res.get('data')
    if (not DblData):
        return Res

    Res = {}
    Dbl = TDbSql().Import(DblData)
    DblOut = Dbl.New()
    DblOut.AddFields(['href'])

    Deep = len(CategoriyIds)
    CategoriyId = CategoriyIds[-1]
    CategoryIds = []
    CategoryInfo = {}
    for Rec in Dbl:
        if (Rec.deep == Deep):
            Data = Rec.GetAsList() + (f'?route=product/category&path={aPath}_{Rec.idt}',)
            DblOut.RecAdd(Data)
            CategoryIds.append(Rec.id)
        elif (Rec.idt == CategoriyId):
            CategoryInfo = Rec.GetAsDict()

    if (DblOut.GetSize() > 0):
        Res['dbl_category'] = DblOut.Export()
    else:
        CategoryIds.append(CategoryInfo.get('id'))

    Res['category'] = CategoryInfo.get('title')
    Products = CategoryInfo.get('products')
    if (not Products):
        return Res

    PageCount = Products // aLimit
    #Pages = [f'route=product/category&path={aPath}&page={i+1}' for i in range(PageCount)]
    #DblPage = TDbSql(['page'], [Pages])
    #ResCategory['dbl_pages'] = DblPage.Export()
    Res['pages'] = list(range(1, PageCount + 1))

    ResProduct = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_CategoriesProducts_LangImagePrice',
            'param': {'aCategoryIds': CategoryIds, 'aLangId': aLangId, 'aPriceId': 1, 'aLimit': aLimit, 'aOffset': aPage * aLimit}
        }
    )

    DblData = ResProduct.get('data')
    if (DblData):
        Dbl = TDbSql().Import(DblData)
        Images = Dbl.ExportStr(['tenant_id', 'image'], '{}/{}')
        ResThumbs = await self.ExecImg('system',
            {
                'method': 'Thumbs',
                'param': {'aFiles': Images}
            }
        )
        Dbl.AddFields(['thumb'], [ResThumbs['thumb']])
        Res['dbl_product'] = Dbl.Export()

    return Res
