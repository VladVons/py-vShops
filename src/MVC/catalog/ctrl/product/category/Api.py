# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import math
#
from IncP.LibCtrl import TDbSql, TDbList, GetDictDefs


async def GetCategory0(self, aData: dict = None) -> dict:
    aLang, = GetDictDefs(
        aData,
        ('lang',),
        ('ua',)
    )

    Label = aData.get('label', '')
    ArrLabel = Label.split('_')
    CategoryId = ArrLabel[-1]
    Res = await self.ExecModel(
        'ref_product0/category',
        {
            'method': 'Get_CategoriesSubCount_ParentLang',
            'param': {'aLang': aLang, 'aParentIdRoot': 0, 'aParentIds': [CategoryId]}
        }
    )

    Items = []
    DblData = Res.get('data')
    Dbl = TDbSql().Import(DblData)
    for Rec in Dbl:
        Path = '_'.join(ArrLabel)
        Href = f'?route=product/category&path={Path}_{Rec.id}'
        Items.append([Rec.title, Href, f'{Label}_{Rec.id}'])

    Res = {
        "menu": {
            'lang': 'ua',
            'level': len(ArrLabel),
            'label': Label,
            'items': TDbList(['name', 'href', 'label'], Items).Export()
        }
    }
    return Res

async def GetCategory(self, aData: dict = None) -> dict:
    aPath, aTenantId, aLang = GetDictDefs(
        aData,
        ('path', 'tenant', 'lang'),
        ('0', 1, 'ua')
    )

    Label = aData.get('label', '')
    ArrLabel = Label.split('_')
    CategoryIdt = ArrLabel[-1]
    Res = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_CategoriesSubCount_TenantParentLang',
            'param': {'aTenantId': aTenantId, 'aLang': aLang, 'aParentIdtRoot': 0, 'aParentIdts': [CategoryIdt]}
        }
    )

    Items = []
    DblData = Res.get('data')
    Dbl = TDbSql().Import(DblData)
    for Rec in Dbl:
        Path = '_'.join(ArrLabel)
        Href = f'?route=product/category&path={Path}_{Rec.idt}&tenant={aTenantId}'
        Items.append([Rec.title, Href, f'{Label}_{Rec.idt}'])

    Res = {
        "menu": {
            'lang': 'ua',
            'level': len(ArrLabel),
            'label': Label,
            'items': TDbList(['name', 'href', 'label'], Items).Export()
        }
    }
    return Res

async def ApiNav(self, aData: dict = None) -> dict:
    if (aData.get('tenant')):
        Res = await GetCategory(self, aData)
    else:
        Res = await GetCategory0(self, aData)
    return Res

async def Main_(self, aData: dict = None) -> dict:
    aPath, aTenantId, aLang, aSort, aOrder, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('path', 'tenant', 'lang', 'sort', 'order', 'page', 'limit'),
        ('0', 1, 'ua', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 15)
    )
    aLimit = min(100, aLimit)

    CategoryIdts = list(map(int, aPath.split('_')))
    Res = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_CategoriesSubCount_TenantParentLang',
            'param': {'aTenantId': aTenantId, 'aLang': aLang, 'aParentIdtRoot': 0, 'aParentIdts': CategoryIdts},
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

    Deep = len(CategoryIdts)
    CategoryIdt = CategoryIdts[-1]
    CategoryInfo = {}
    Products = 0
    for Rec in DblCategory:
        if (Rec.deep == Deep):
            Data = Rec.GetAsList() + (f'?route=product/category&path={aPath}_{Rec.idt}&tenant={aTenantId}',)
            DblOut.RecAdd(Data)
            Products += Rec.products
        elif (Rec.idt == CategoryIdt):
            CategoryInfo = Rec.GetAsDict()

    Products = CategoryInfo.get('products', Products)
    Res['products'] = Products
    Res['category'] = CategoryInfo.get('title', '/')
    if (not Products):
        return Res

    Res['pages'] = math.ceil(Products / aLimit)

    if (CategoryIdt == 0):
        CategoryIdt = [Rec.idt for Rec in DblCategory if Rec.parent_idt == 0]
    else:
        CategoryIdt = [CategoryIdt]

    ResEM = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_CategoryIdtsTenant_Sub',
            'param': {'aCategoryIdts': CategoryIdt, 'aTenantId': aTenantId}
        }
    )
    DblData = ResEM.get('data')
    Dbl = TDbSql().Import(DblData)
    if (DblOut.GetSize() > 0):
        Res['dbl_category'] = DblOut.Export()
        CategoryIds = Dbl.ExportList('id')
    else:
        Id = CategoryInfo.get('id')
        CategoryIds = [Id]

    ResProduct = await self.ExecModel(
        'ref_product/category',
        {
            'method': 'Get_CategoriesProducts0_LangImagePrice',
            'param': {'aCategoryIds': CategoryIds, 'aLang': aLang, 'aPriceId': 1, 'aOrder': f'{aSort} {aOrder}', 'aLimit': aLimit, 'aOffset': (aPage - 1) * aLimit}
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
            Href = f'?route=product/product&path={aPath}&product_id={Rec.product_id}&tenant={aTenantId}'
            Hrefs.append(Href)

        DblProduct.AddFields(['thumb', 'href'], [ResThumbs['thumb'], Hrefs])
        Res['dbl_product'] = DblProduct.Export()
        Res['title'] = '---category---'

    return Res

async def Main(self, aData: dict = None) -> dict:
    aPath, aLang, aSort, aOrder, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('path', 'lang', 'sort', 'order', 'page', 'limit'),
        ('0', 'ua', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 15)
    )
    aLimit = min(100, aLimit)

    CategoryIds = list(map(int, aPath.split('_')))
    Res = await self.ExecModel(
        'ref_product0/category',
        {
            'method': 'Get_CategoriesSubCount_ParentLang',
            'param': {'aLang': aLang, 'aParentIdRoot': 0, 'aParentIds': CategoryIds}
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
    Products = 0
    for Rec in DblCategory:
        if (Rec.deep == Deep):
            Data = Rec.GetAsList() + (f'?route=product/category&path={aPath}_{Rec.id}',)
            DblOut.RecAdd(Data)
            Products += Rec.products
        elif (Rec.id == CategoryId):
            CategoryInfo = Rec.GetAsDict()

    Products = CategoryInfo.get('products', Products)
    Res['products'] = Products
    Res['category'] = CategoryInfo.get('title', '/')
    if (not Products):
        return Res

    Res['pages'] = math.ceil(Products / aLimit)

    if (CategoryId == 0):
        CategoryId = [Rec.id for Rec in DblCategory if Rec.parent_id == 0]
    else:
        CategoryId = [CategoryId]

    ResEM = await self.ExecModel(
        'ref_product0/category',
        {
            'method': 'Get_CategoryIds_Sub',
            'param': {'aCategoryIds': CategoryId}
        }
    )
    DblData = ResEM.get('data')
    Dbl = TDbSql().Import(DblData)
    if (DblOut.GetSize() > 0):
        Res['dbl_category'] = DblOut.Export()
        CategoryIds = Dbl.ExportList('id')
    else:
        Id = CategoryInfo.get('id')
        CategoryIds = [Id]

    ResProduct = await self.ExecModel(
        'ref_product0/category',
        {
            'method': 'Get_CategoriesProducts_LangImagePrice',
            'param': {'aCategoryIds': CategoryIds, 'aLang': aLang, 'aPriceId': 1, 'aOrder': f'{aSort} {aOrder}', 'aLimit': aLimit, 'aOffset': (aPage - 1) * aLimit}
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
            Href = f'?route=product/product&path={aPath}&product_id={Rec.product_id}'
            Hrefs.append(Href)

        DblProduct.AddFields(['thumb', 'href'], [ResThumbs['thumb'], Hrefs])
        Res['dbl_product'] = DblProduct.Export()
        Res['title'] = '---category---'

    return Res
