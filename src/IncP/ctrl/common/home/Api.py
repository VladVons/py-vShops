# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


__all__ = ['Main']


async def Main(aParent, aQuery: dict = None) -> dict:
    Res = {}

    Res['category'] = await aParent.Master.Get(
        'ref_product/category',
        {
            "method": "GetCategoriesByParent",
            "param": {'aTenantId': 1, 'aParentId': 0, 'aDepth': 1}
        }
    )

    return Res
