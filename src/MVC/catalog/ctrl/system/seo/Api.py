# Created: 2024.03.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
from IncP.LibCtrl import GetDictDefs


async def Decode(self, aData: dict) -> dict:
    aLang, aPath = GetDictDefs(aData,
        ('lang', 'path'),
        ('ua', '')
    )
    return aPath

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
    return aPath

    AttrVal = set()
    Parsed = []
    for xPath in aPath:
        Pairs = xPath.strip('/?').split('&')
        ArrPair = []
        for xPair in Pairs:
            ArrPair.append(xPair)
            Key, Val = xPair.split('=')
            AttrVal.add((Key, Val))
        Parsed.append(ArrPair)

    aLangId = self.GetLangId(aLang)
    Dbl = await self.ExecModelImport(
        'system',
        {
            'method': 'Get_SeoFromDict',
            'param': {
                'aLangId': aLangId,
                'aAttrVal': AttrVal
            }
        }
    )

    Pairs = Dbl.ExportPair('attr_val', 'keyword')
    Res = []
    for Idx, xPath in enumerate(Parsed):
        Arr = [Pairs.get(x, f'&{x}') for x in xPath]
        if (Arr[0].startswith('&')):
            Res.append(aPath[Idx])
        else:
            Res.append('/'.join(Arr).replace('/&', '&'))
    return Res
