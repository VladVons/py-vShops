# Created: 2023.11.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from IncP.LibCtrl import TDbList


async def Main(self, aDbl: TDbList) -> TDbList:
    Missed = aDbl.Rec.GetFieldsMissed(['image', 'category_id', 'category_title', 'product_id', 'tenant_id'])
    assert (not Missed), f'Missed fields {Missed}'

    Images = aDbl.ExportStr(['image'], 'product/{}')
    ResThumbs = await self.ExecImg(
        'system',
        {
            'method': 'GetThumbs',
            'param': {'aFiles': Images}
        }
    )

    aDbl.AddFieldsFill(['thumb', 'product_href', 'category_href', 'tenant_href'], False)
    for Thumb, Rec in zip(ResThumbs['thumb'], aDbl, strict=True):
        New = [
            Thumb,
            f'?route=product0/product&product_id={Rec.product_id}',
            f'?route=product0/category&category_id={Rec.category_id}',
            f'?tenant={Rec.tenant_id}'
        ]
        aDbl.RecMerge(New)
    return aDbl
