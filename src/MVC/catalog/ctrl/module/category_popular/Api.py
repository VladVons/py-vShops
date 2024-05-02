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
        Hrefs = [f'/?route=product0/category&category_id={Rec.id}' for Rec in Dbl]
        if (self.ApiCtrl.Conf.get('seo_url')):
            Hrefs = await Lib.SeoEncodeList(self, Hrefs)

        Images = Dbl.ExportStr(['image'], 'category/{}')
        ResThumbs = await self.ExecImg(
            'system',
            {
                'method': 'GetThumbs',
                'param': {'aFiles': Images}
            }
        )

        Dbl.AddFieldsFill(['thumb', 'href'], False)
        Zip = zip(ResThumbs['thumb'], Hrefs, Dbl, strict=True)
        for Thumb, Href, Rec in Zip:
            Dbl.RecMerge([Thumb, Href])

        return {
            'dbl_category_popular': Dbl.Export()
        }
