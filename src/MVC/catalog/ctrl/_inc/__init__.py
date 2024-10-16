# Created: 2023.12.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def GetBreadcrumbs(self, aLangId: str, aCategoryId: int) -> list:
    Res = []
    if (aCategoryId):
        Dbl = await self.ExecModelImport(
            'ref_product0/category',
            {
                'method': 'Get_CategoryId_Path',
                'param': {
                    'aLangId': aLangId,
                    'aCategoryIds': [aCategoryId]
                }
            }
        )
        if (Dbl):
            Hrefs = [f'/?route=product0/category&category_id={Id}' for Id in Dbl.Rec.path_id]
            #Hrefs.insert(0, '/?route=product0/category&category_id=0')
            if (self.ApiCtrl.Conf.get('seo_url')):
                Hrefs = await Lib.SeoEncodeList(self, Hrefs)

            for Idx, Title in enumerate(Dbl.Rec.path_title):
                Res.append({'href': Hrefs[Idx], 'title': Title})

    return Res

def GetProductsSort(aHref: str, aCur: str, aLang: dict) -> Lib.TDbList:
    Dbl = Lib.TDbList().Import({
        'head': ['href', 'title', 'selected'],
        'data': [
            [f'{aHref}', aLang.get('default', '-default-'), ''],
            [Lib.UrlUdate(aHref, {'sort': 'title', 'order': 'asc'}), aLang.get('name_az'),  ''],
            [Lib.UrlUdate(aHref, {'sort': 'title', 'order': 'desc'}), aLang.get('name_za'),  ''],
            [Lib.UrlUdate(aHref, {'sort': 'price', 'order': 'asc'}), aLang.get('price_19'), ''],
            [Lib.UrlUdate(aHref, {'sort': 'price', 'order': 'desc'}), aLang.get('price_91'), '']
        ]
    })
    for Rec in Dbl:
        if (aCur in Rec.href):
            Rec.SetField('selected', 'selected')
    return Dbl
