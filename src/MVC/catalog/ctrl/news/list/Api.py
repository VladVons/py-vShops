# Created: 2024.03.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    aLang, aPage, aLimit = Lib.GetDictDefs(
        aData.get('query'),
        ('lang', 'page', 'limit'),
        ('ua', 1, 20)
    )

    if (not Lib.IsDigits([aPage, aLimit])):
        return {'status_code': 404}

    aLimit = max(aLimit, 50)
    aLangId = self.GetLangId(aLang)
    Dbl = await self.ExecModelImport(
        'ref_news',
        {
            'method': 'Get_List',
            'param': {
                'aLangId': aLangId,
                'aGroupId': 1, 
                'aLimit': aLimit,
                'aOffset': (aPage - 1) * aLimit
            }
        }
    )
    if (not Dbl):
        return {'status_code': 404}

    Href = aData['path_qs']
    #Href = UrlEncode(aData['query'])

    Pagination = Lib.TPagination(aLimit, Href)
    PData = Pagination.Get(Dbl.Rec.total, aPage)
    DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)

    Hrefs = [f'/?route=news/item&news_id={Rec.id}' for Rec in Dbl]
    if (self.ApiCtrl.Conf.get('seo_url')):
        Hrefs = await Lib.SeoEncodeList(self, Hrefs)

    Dbl.AddFieldsFill(['href'], False)
    for Idx, Rec in enumerate(Dbl):
        Dbl.RecMerge([Hrefs[Idx]])

    return {
        'dbl_news': Dbl.Export(),
        'dbl_pagenation': DblPagination.Export()
    }
