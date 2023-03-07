# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Loader.Lang import TLoaderLangFs


__all__ = ['Main']


async def Main(aParent, aQuery: dict = None) -> dict:
    Lang = TLoaderLangFs('ua', 'MVC/Lang')
    await Lang.Add('common/home')
    ToDo = Lang.Get('service')

    Res = {}

    Res['category'] = await aParent.Master.Get(
        'ref_product/category',
        {
            "method": "GetCategoriesByParent",
            "param": {'aTenantId': 1, 'aParentIdt': 0, 'aDepth': 1}
        }
    )

    return Res
