# Created: 2023.04.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbSql, GetDictDefs


async def ApiOrder(self, aData: dict = None) -> dict:
    Res = {
        'status': 'ok',
        'order_id': 54725
    }
    return Res

async def Main(self, aData: dict = None) -> dict:
    Res = {}

    Res['href'] = {
        'confirm': '?route=checkout/confirm'
    }

    return Res
