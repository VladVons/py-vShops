# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from IncP.LibCtrl import TDbSql, GetDictDef


async def Main(self, aData: dict = None) -> dict:
    aSearch, aLangId, aPage, aLimit = GetDictDef(
        aData.get('query'),
        ('search', 'lang', 'page', 'limit'),
        ('', 1, 0, 15), True
    )

    Res = await self.ExecModel(
        'ref_product/product',
        {
            'method': 'Get_Products_LangFilter',
            'param': {'aLangId': aLangId, 'aFilter': aSearch, 'aLimit': aLimit, 'aOffset': aPage * aLimit}
        }
    )

    DblData = Res.get('data')
    if (DblData):
        Dbl = TDbSql().Import(DblData)
        Res['total'] = Dbl.Rec.total
        Res['dbl_product'] = Res.pop('data')

        PageCount = Dbl.Rec.total // aLimit
        Res['pages'] = list(range(1, PageCount + 1))
    else:
        Res['total'] = 0
    Res['search'] = aSearch
    return Res
