# Created: 2024.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def ajax(self, aData: dict = None) -> dict:
    Post = aData.get('post')
    if (not Post):
        return

    if (Post['items']):
        Dbl = await self.ExecModelImport(
            'ref_product0/category',
            {
                'method': 'Get_CategoryAttrFilter',
                'param': {
                    'aLangId': Post['lang_id'],
                    'aCategoryId': Post['category_id'],
                    'aAttr': Post['items']
                }
            }
        )
        return Dbl.Export()

async def Main(self, aData: dict = None) -> dict:
    aCategoryId, aLang, aAttr = Lib.GetDictDefs(
        aData.get('query'),
        ('category_id', 'lang', 'attr'),
        ('0', 'ua', '')
    )

    if (not Lib.IsDigits([aCategoryId])):
        return {'status_code': 404}

    aLangId = self.GetLangId(aLang)

    Dbl = await self.ExecModelImport(
        'ref_product0/category',
        {
            'method': 'Get_CategoryAttr',
            'param': {
                'aLangId': aLangId,
                'aCategoryId': aCategoryId
            }
        }
    )

    if (Dbl):
        AttrPair = Dbl.ExportPair('attr_id', 'title')
        Attr = Lib.AttrDecode(aAttr)
        AttrArr = [AttrPair.get(int(Key), '') + ': ' + ';'.join(Val) for Key, Val in Attr.items()]

        return {
            'category_id': aCategoryId,
            'lang_id': aLangId,
            'dbl_category_attr': Dbl.Export(),
            'descr': ', '.join(AttrArr)
        }
