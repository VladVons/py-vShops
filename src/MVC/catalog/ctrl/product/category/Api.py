# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import math
#
from IncP.LibCtrl import TDbSql, GetDictDefs


async def Main(self, aData: dict = None) -> dict:
    aPath, aTenantId, aLangId, aSort, aOrder, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('path', 'tenant', 'lang', 'sort', 'order', 'page', 'limit'),
        ('0', 1, 1, ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 15)
    )
    aLimit = min(100, aLimit)

    CategoryIds = list(map(int, aPath.split('_')))
    Res = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_CategoriesSubCount_TenantParentLang',
            'param': {'aTenantId': aTenantId, 'aLangId': aLangId, 'aParentIdtRoot': 0, 'aParentIdts': CategoryIds},
            'query': True
        }
    )
    DblData = Res.get('data')
    if (not DblData):
        return Res
    #print(Res['query'])

    Res = {}
    DblCategory = TDbSql().Import(DblData)

    DblOut = DblCategory.New()
    DblOut.AddFields(['href'])

    Deep = len(CategoryIds)
    CategoryId = CategoryIds[-1]
    CategoryInfo = {}
    for Rec in DblCategory:
        if (Rec.deep == Deep):
            Data = Rec.GetAsList() + (f'?route=product/category&path={aPath}_{Rec.idt}&tenant={aTenantId}',)
            DblOut.RecAdd(Data)
        elif (Rec.idt == CategoryId):
            CategoryInfo = Rec.GetAsDict()

    Res['category'] = CategoryInfo.get('title')
    Products = CategoryInfo.get('products')
    if (not Products):
        return Res

    Res['products'] = Products
    Res['pages'] = math.ceil(Products / aLimit)

    ResEM = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_CategoryIdtTenant_Sub',
            'param': {'aCategoryIdt': CategoryId, 'aTenantId': aTenantId}
        }
    )

    DblData = ResEM.get('data')
    Dbl = TDbSql().Import(DblData)
    if (Dbl.GetSize() > 0):
        Res['dbl_category'] = DblOut.Export()
        CategoryIds = Dbl.ExportList('id')
        CategoryIdToPath = Dbl.ExportPair('id', 'path_idt')
    else:
        Id = CategoryInfo.get('id')
        CategoryIds = [Id]
        CategoryIdToPath = {Id: CategoryInfo.get('path_idt')}

    ResProduct = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_CategoriesProducts0_LangImagePrice',
            'param': {'aCategoryIds': CategoryIds, 'aLangId': aLangId, 'aPriceId': 1, 'aOrder': f'{aSort} {aOrder}', 'aLimit': aLimit, 'aOffset': (aPage - 1) * aLimit},
        }
    )
    DblData = ResProduct.get('data')
    if (DblData):
        DblProduct = TDbSql().Import(DblData)

        Images = DblProduct.ExportStr(['image'], 'product/{}')
        ResThumbs = await self.ExecImg(
            'system',
            {
                'method': 'GetThumbs',
                'param': {'aFiles': Images}
            }
        )

        Hrefs = []
        for Rec in DblProduct:
            Path = f'0_{CategoryId}_'.join(map(str, CategoryIdToPath[Rec.category_id]))
            Href = f'?route=product/product&path={Path}&product_id={Rec.product_id}&tenant={aTenantId}'
            Hrefs.append(Href)

        DblProduct.AddFields(['thumb', 'href'], [ResThumbs['thumb'], Hrefs])
        Res['dbl_product'] = DblProduct.Export()

    return Res
