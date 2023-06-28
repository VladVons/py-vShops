# Created: 2023.04.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbSql, GetDictDefs
from .Features import TFeatures


async def Main(self, aData: dict = None) -> dict:
    aLangId, aProductId = GetDictDefs(
        aData.get('query'),
        ('lang', 'product_id'),
        (1, 0)
    )

    Res = await self.ExecModel(
        'ref_product/product',
        {
            'method': 'Get_Product0_LangId',
            'param': {'aLangId': aLangId, 'aProductId': aProductId},
            'query': True
        }
    )
    #print(Res.get('query'))

    DblData = Res.get('data')
    if (DblData):
        Dbl = TDbSql().Import(DblData)

        Images = [f'product/{x}' for x in Dbl.Rec.images]
        ResImg = await self.ExecImg(
            'system',
            {
                'method': 'GetImages',
                'param': {'aFiles': Images}
            }
        )
        Images = ResImg['image']
        if (Images):
            Res['image'] = Images[0]
            Res['images'] = Images
        else:
            Res['image'] = 'no image'

        Res['product'] = Dbl.Rec.GetAsDict()

        Features = Res['product'].get('features', {})
        Res['product']['features'] = TFeatures(aLangId).Adjust(Features)

        del Res['data']
    return Res
