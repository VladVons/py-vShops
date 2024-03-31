# Created: 2023.09.09
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    aOrderId, aLang = Lib.GetDictDefs(
        aData.get('query'),
        ('order_id', 'lang'),
        ('', 'ua')
    )

    Res = {
        'doc_attr': None,
        'doc_table': None,
        'href': {
            'confirm': '/?route=checkout/orders&customer_id=1'
        }
    }

    if (aOrderId):
        DblOrderMix = await self.ExecModelImport(
            'doc_sale',
            {
                'method': 'Get_OrderMix',
                'param': {'aOrderId': aOrderId}
            }
        )

        if (DblOrderMix):
            Res['doc_attr'] = DblOrderMix.Rec.GetAsDict()

            DblOrderMixTable = await self.ExecModelImport(
                'doc_sale',
                {
                    'method': 'Get_OrderMixTableProduct',
                    'param': {'aOrderId': aOrderId, 'aLang': aLang}
                }
            )

            if (DblOrderMixTable):
                ProductIds = DblOrderMixTable.ExportList('id')
                DblPathIdt = await self.ExecModelImport(
                    'ref_product/category',
                    {
                        'method': 'Get_ProductIds_PathIdt',
                        'param': {'aProductIds': ProductIds}
                    }
                )
                IdPairs = DblPathIdt.ExportPairs('id', ['path_idt', 'tenant_id'])

                Images = DblOrderMixTable.ExportStr(['image'], 'product/{}')
                Thumbs = await self.ExecImg(
                    'system',
                    {
                        'method': 'GetThumbs',
                        'param': {'aFiles': Images}
                    }
                )
                DblOrderMixTable.ToList().AddFields(['href', 'thumb'])
                for Rec, Thumb in zip(DblOrderMixTable, Thumbs['thumb']):
                    Rec.SetField('thumb', Thumb)

                    PathArr, TenantId = IdPairs[Rec.id]
                    Path = "_".join(map(str, PathArr))
                    Href = f'/?route=product/product&path={Path}&product_id={Rec.id}&tenant={TenantId}'
                    Rec.SetField('href', Href)

                Res['doc_table'] = DblOrderMixTable.Export()
    return Res
