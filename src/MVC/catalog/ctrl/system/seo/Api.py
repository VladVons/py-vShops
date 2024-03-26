# Created: 2024.03.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs


async def Decode(self, aData: dict) -> dict:
    aLang, aPath = GetDictDefs(aData,
        ('lang', 'path'),
        ('ua', '')
    )

    aLangId = self.GetLangId(aLang)
    Dbl = await self.ExecModelImport(
        'system',
        {
            'method': 'Get_SeoToDict',
            'param': {
                'aLangId': aLangId,
                'aPath': aPath.split('/')
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

    AttrVal = set()
    Parsed = []
    for xPath in aPath:
        Pairs = xPath.split('&')
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

    Arr = [Pairs.get(x, x) x in Parsed]
    return
