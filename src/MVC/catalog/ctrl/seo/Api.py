# Created: 2024.03.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
import IncP.LibCtrl as Lib


async def Decode(self, aData: dict) -> dict:
    aPath = aData.get('path', [])

    if (not self.ApiCtrl.Conf['seo_url']):
        return aPath

    Values = re.split(r'[/&]', aPath)
    Dbl = await self.ExecModelImport(
        'ref_seo',
        {
            'method': 'Get_SeoToDict',
            'param': {
                'aPath': Values
            }
        }
    )

    Arr = [f'{Rec.attr}={Rec.val}' for Rec in Dbl]
    return '&'.join(Arr)

async def Encode(self, aData: dict) -> dict:
    aPath = aData.get('path', [])

    if (not self.ApiCtrl.Conf['seo_url']):
        return aPath

    # aPath = [
    #     '/?route=product0/tenant&tenant_id=1',
    #     'page=2&order=2&route=product0/category&category_id=2',
    #     'route=product0/category&page=1&category_id=1'
    # ]

    Data = []
    for Idx, xPath in enumerate(aPath):
        Pairs = xPath.strip('/?').split('&')
        for xPair in Pairs:
            if (xPair.count('=') == 1):
                Key, Val = xPair.split('=')
            else:
                Key = Val = xPair
            Data.append((Key, Val, Idx))

    Dbl = await self.ExecModelImport(
        'ref_seo',
        {
            'method': 'Get_SeoFromDict',
            'param': {
                'aData': Data
            }
        }
    )

    Res = []
    for Rec in Dbl:
        Url = ''
        for Path, Query in Rec.url:
            if (Path):
                Url += '/' + Path
            else:
                Url += Lib.Iif('?' in Url, '&', '?') + Query
        Res.append(Url.lstrip('&'))
    return Res

async def Redirect(self, aData: dict) -> dict:
    aPath = aData.get('path')
    Dbl = await self.ExecModelImport(
        'ref_seo',
        {
            'method': 'Get_SeoRedirect',
            'param': {
                'aPath': aPath
            }
        }
    )
    if (Dbl):
        return Dbl.Rec.url_new
