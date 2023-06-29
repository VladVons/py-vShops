# Created: 2023.04.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbSql, GetDictDefs
from .Features import TFeatures


async def Main(self, aData: dict = None) -> dict:
    async def GetPrice(aProductId: int) -> dict:
        Res = await self.ExecModel(
            'ref_product/price',
            {
                'method': 'Get_Price_Product',
                'param': {'aProductId': aProductId}
            }
        )

        DblData = Res.get('data')
        if (DblData):
            Dbl = TDbSql().Import(DblData)
            return Dbl.Export()

    async def GetPriceHist(aProductId: int) -> dict:
        Res = await self.ExecModel(
            'ref_product/price',
            {
                'method': 'Get_PriceHist_Product',
                'param': {'aProductId': aProductId}
            }
        )

        DblData = Res.get('data')
        if (DblData):
            Dbl = TDbSql().Import(DblData)
            return Dbl.Export()

    async def GetImages(aImages: list[str]) -> dict:
        Images = [f'product/{x}' for x in aImages]
        ResEI = await self.ExecImg(
            'system',
            {
                'method': 'GetImages',
                'param': {'aFiles': Images}
            }
        )

        Images = ResEI['image']
        if (Images):
            Res = {'image': Images[0], 'images': Images}
        else:
            Res = {'image': 'http://ToDo/NoImage.jpg', 'images': []}
        return Res

    aLangId, aProductId = GetDictDefs(
        aData.get('query'),
        ('lang', 'product_id'),
        (1, 0)
    )

    Res = await self.ExecModel(
        'ref_product/product',
        {
            'method': 'Get_Product0_LangId',
            'param': {'aLangId': aLangId, 'aProductId': aProductId}
        }
    )

    DblData = Res.get('data')
    if (DblData):
        del Res['data']

        Dbl = TDbSql().Import(DblData)
        Product = Dbl.Rec.GetAsDict()

        Features = Product.get('features', {})
        Product['features'] = TFeatures(aLangId).Adjust(Features)

        Images = await GetImages(Dbl.Rec.images)
        Product.update(Images)

        Product['price'] = await GetPrice(aProductId)
        Product['price_hist'] = await GetPriceHist(aProductId)

        Res['product'] = Product
    return Res
