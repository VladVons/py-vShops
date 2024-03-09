# Created: 2023.12.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbList


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
            #Res.append({'href': '?route=product0/category&category_id=0', 'title': '/'})
            for Title, Id in zip(Dbl.Rec.path_title, Dbl.Rec.path_id):
                Res.append({'href': f'?route=product0/category&category_id={Id}', 'title': Title})
    return Res

def GetProductsSort(aHref: str, aCur: str, aLang: dict) -> TDbList:
    Dbl = TDbList().Import({
        'head': ['href', 'title', 'selected'],
        'data': [
            [f'{aHref}', aLang.get('default', '-default-'), ''],
            [f'{aHref}&sort=title&order=asc',  aLang.get('name_az'),  ''],
            [f'{aHref}&sort=title&order=desc', aLang.get('name_za'),  ''],
            [f'{aHref}&sort=price&order=asc',  aLang.get('price_19'), ''],
            [f'{aHref}&sort=price&order=desc', aLang.get('price_91'), '']
        ]
    })
    for Rec in Dbl:
        if (aCur in Rec.href):
            Rec.SetField('selected', 'selected')
    return Dbl
