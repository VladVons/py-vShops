# Created: 2024.03.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
from IncP.LibCtrl import GetDictDefs, Iif


async def Decode(self, aData: dict) -> dict:
    aLang, aPath = GetDictDefs(aData,
        ('lang', 'path'),
        ('ua', '')
    )
    #return aPath

    Values = re.split(r'[/&]', aPath)
    aLangId = self.GetLangId(aLang)
    Dbl = await self.ExecModelImport(
        'system',
        {
            'method': 'Get_SeoToDict',
            'param': {
                'aLangId': aLangId,
                'aPath': Values
            }
        }
    )

    Arr = [f'{Rec.attr}={Rec.val}' for Rec in Dbl]
    return '&'.join(Arr)

async def Encode(self, aData: dict) -> dict:
    aLang, aPath = GetDictDefs(aData,
        ('lang', 'path'),
        ('ua', [])
    )
    #return aPath
    # aPath = [
    #     '/?route=product0/tenant&tenant_id=1',
    #     'page=2&order=2&route=product0/category&category_id=2',
    #     'route=product0/category&page=1&category_id=1'
    # ]

    Data = []
    for Idx, xPath in enumerate(aPath):
        Pairs = xPath.strip('/?').split('&')
        for xPair in Pairs:
            Key, Val = xPair.split('=')
            Data.append((Key, Val, Idx))

    aLangId = self.GetLangId(aLang)
    Dbl = await self.ExecModelImport(
        'system',
        {
            'method': 'Get_SeoFromDict',
            'param': {
                'aLangId': aLangId,
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
                Url += Iif('?' in Url, '&', '?') + Query
        Res.append(Url.lstrip('&'))
    return Res
