# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import math
#
from IncP.LibCtrl import TDbSql, GetDictDefs


async def Main(self, aData: dict = None) -> dict:
    await self.Lang.Add('product/category')

    aSearch, aLangId, aSort, aOrder, aPage, aLimit = GetDictDefs(
        aData.get('query'),
        ('search', 'lang', 'sort', 'order', 'page', 'limit'),
        ('', 1, ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 15)
    )
    aLimit = min(100, aLimit)

    ResProduct = await self.ExecModel(
        'ref_product/product',
        {
            'method': 'Get_Products0_LangFilter',
            'param': {'aLangId': aLangId, 'aFilter': aSearch, 'aOrder': f'{aSort} {aOrder}', 'aLimit': aLimit, 'aOffset': (aPage - 1) * aLimit},
            'query': True
        }
    )
    print(ResProduct.get('query'))

    DblProduct = ResProduct.get('data')
    if (DblProduct):
        DblProduct = TDbSql().Import(DblProduct)
        CategoryIds = DblProduct.ExportList('category_id', True)
        ResCategory = await self.ExecModel(
            'ref_product/category',
            {
                'method': 'Get_CategoryPath_Lang',
                'param': {'aLangId': aLangId, 'aIds': CategoryIds}
            }
        )
        DblCategory = TDbSql().Import(ResCategory.get('data'))

        CategoryIdToPath = DblCategory.ExportPair('id', 'path_idt')
        Hrefs = []
        for Rec in DblProduct:
            Path = '0_' + '_'.join(map(str, CategoryIdToPath[Rec.category_id]))
            Href = f'?route=product/product&path={Path}&product_id={Rec.product_id}'
            Hrefs.append(Href)

        Images = DblProduct.ExportStr(['image'], 'product/{}')
        ResThumbs = await self.ExecImg('system',
            {
                'method': 'GetThumbs',
                'param': {'aFiles': Images}
            }
        )
        DblProduct.AddFields(['thumb', 'href'], [ResThumbs['thumb'], Hrefs])
        ResProduct['dbl_product'] = DblProduct.Export()

        ResProduct['pages'] = math.ceil(DblProduct.Rec.total / aLimit)
        ResProduct['total'] = DblProduct.Rec.total

        del ResProduct['data']
    else:
        ResProduct['total'] = 0
    ResProduct['search'] = aSearch

    return ResProduct
