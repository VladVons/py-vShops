# Created: 2023.12.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


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
            for Title, Id in zip(Dbl.Rec.path_title, Dbl.Rec.path_id):
                Res.append({'href': f'?route=product0/category&category_id={Id}', 'title': Title})
    return Res
