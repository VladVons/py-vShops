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
            'param': {'aLang': aLang, 'aLimit': 12}
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

        ProductHref = []
        CategoryHref = []
        TenantHref = []


        for Rec in Dbl:
            Path = '0_' + '_'.join(map(str, Rec.path_id))
            Href = f'?route=product/product&product_id={Rec.product_id}&path={Path}'
            ProductHref.append(Href)

            Href = f'?route=product/category&path={Path}'
            CategoryHref.append(Href)

            Href = f'?tenant={Rec.tenant_id}'
            TenantHref.append(Href)

        Dbl.AddFields(['thumb', 'product_href', 'category_href', 'tenant_href'],
                      [ResThumbs['thumb'], ProductHref, CategoryHref, TenantHref])
        Res['data'] = Dbl.Export()
    return Res
