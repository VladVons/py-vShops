# Created: 2023.11.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbList


async def Main(self, aDbl: TDbList) -> TDbList:
    Missed = aDbl.Rec.GetFieldsMissed(['id', 'category_id', 'category_title', 'image'])
    assert not Missed, f'Missed fields {Missed}'

    Images = aDbl.ExportStr(['image'], 'product/{}')
    ResThumbs = await self.ExecImg(
        'system',
        {
            'method': 'GetThumbs',
            'param': {'aFiles': Images}
        }
    )

    ProductHref = []
    CategoryHref = []

    for Rec in aDbl:
        Href = f'/{self.Name}/?route=product/product&product_id={Rec.id}'
        ProductHref.append(Href)

        Href = f'/{self.Name}/?route=product/category&category_id={Rec.category_id}'
        CategoryHref.append(Href)

    aDbl.AddFields(['thumb', 'product_href', 'category_href'],
                    [ResThumbs['thumb'], ProductHref, CategoryHref])
    return aDbl
