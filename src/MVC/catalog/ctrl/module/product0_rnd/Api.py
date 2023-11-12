# Created: 2023.10.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDef, TDbSql


async def Main(self, aData: dict = None) -> dict:
    aLang, = GetDictDef(
        aData.get('query'),
        ('lang',),
        ('ua',)
    )

    Res = await self.ExecModel(
        'ref_product0/product',
        {
            'method': 'Get_ProductsRnd_LangImagePrice',
            'param': {'aLang': aLang, 'aLimit': 24}
        }
    )

    DblData = Res.get('data')
    if (DblData):
        Dbl = TDbSql().Import(DblData)

        Images = Dbl.ExportStr(['image'], 'product/{}')
        ResThumbs = await self.ExecImg(
            'system',
            {
                'method': 'GetThumbs',
                'param': {'aFiles': Images}
            }
        )

        Hrefs = []
        for Rec in Dbl:
            Path = '0_' + '_'.join(map(str, Rec.path_id))
            Href = f'?route=product/product&product_id={Rec.product_id}&path={Path}'
            Hrefs.append(Href)
        Dbl.AddFields(['thumb', 'href'], [ResThumbs['thumb'], Hrefs])
        Res['data'] = Dbl.Export()
    return Res
