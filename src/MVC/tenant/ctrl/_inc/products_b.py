# Created: 2023.11.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbList


async def Main(self, aDbl: TDbList) -> TDbList:
    Missed = aDbl.Rec.GetFieldsMissed(['id', 'category_title', 'image'])
    assert not Missed, f'Missed fields {Missed}'

    Images = aDbl.ExportStr(['image'], 'product/{}')
    ResThumbs = await self.ExecImg(
        'system',
        {
            'method': 'GetThumbs',
            'param': {'aFiles': Images}
        }
    )

    aDbl.AddFieldsFill(['thumb', 'product_href', 'category_href'], False)
    for Thumb, Rec in zip(ResThumbs['thumb'], aDbl, strict=True):
        New = [
            Thumb,
            f'/{self.Name}/tenant/?route=product/product&product_id={Rec.id}',
            f'/{self.Name}/tenant/?route=product/category&category_id={Rec.category_id}'
        ]
        aDbl.RecMerge(New)
    return aDbl
