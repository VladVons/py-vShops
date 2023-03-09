# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Main(self, _aQuery: dict = None) -> dict:
    Res = {}

    await self.Lang.Add('common/home')
    await self.Lang.Add('misc/about')
    #Text = self.Lang.Get('service')
    Res['lang'] = self.Lang.Join()

    Data = await self.ExecModel(
        'ref_product/category',
        {
            "method": "GetCategoriesByParent",
            "param": {'aTenantId': 1, 'aParentIdt': 0, 'aDepth': 1}
        }
    )

    if (Data.get('status') != 200):
        return {'err': Data.get('err')}

    return Res
