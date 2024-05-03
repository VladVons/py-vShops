# Created: 2024.05.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    aLang = Lib.DeepGetByList(aData, ['query', 'lang'], 'ua')
    aLangId = self.GetLangId(aLang)

    Dbl = await self.ExecModelImport(
        'ref_product0/category',
        {
            'method': 'Get_CategoryPopular',
            'param': {
                'aLangId': aLangId,
                'aLimit': 6
            }
        }
    )

    if (Dbl):
        Hrefs = {}
        Href = '/?route=product0/category&category_id='
        for Rec in Dbl:
            Hrefs[Rec.id] = f'{Href}{Rec.id}'
            Childs = Rec.childs
            if (Childs):
                for Id, _Title in Childs:
                    Hrefs[int(Id)] = f'{Href}{Id}'

        if (self.ApiCtrl.Conf.get('seo_url')):
            Hrefs = await Lib.SeoEncodeDict(self, Hrefs)

        Images = Dbl.ExportStr(['image'], 'category/{}')
        ResThumbs = await self.ExecImg(
            'system',
            {
                'method': 'GetThumbs',
                'param': {'aFiles': Images}
            }
        )

        Dbl.AddFieldsFill(['thumb', 'href'], False)
        Zip = zip(ResThumbs['thumb'], Dbl, strict=True)
        for Thumb, Rec in Zip:
            Dbl.RecMerge([Thumb, Hrefs[Rec.id]])
            Childs = Rec.childs
            if (Childs):
                for Idx, xChild in enumerate(Childs):
                    Id = int(xChild[0])
                    Childs[Idx][0] = Hrefs[Id]
                Dbl.Rec.SetField('childs', Childs)
        return {
            'dbl_category_popular': Dbl.Export()
        }
