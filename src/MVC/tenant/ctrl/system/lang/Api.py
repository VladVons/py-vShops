# Created: 2023.03.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs


async def Main(self, aData: dict) -> dict:
    # aLang, aPath, aKey = GetDictDefs(
    #     aData.get('query'),
    #     ('lang', 'path', 'key'),
    #     ('ua', '', 'tpl')
    # )

    aLang, aPath, aKey = GetDictDefs(
        aData,
        ('lang', 'path', 'key'),
        ('ua', '', 'tpl')
    )

    Res = await self.Lang.Add(aLang, aPath, aKey)
    #Res = self.Lang.Join()
    return Res


async def GetLangs(self, _aData: dict) -> dict:
    Dbl = await self.ExecModelImport(
        'system',
        {
            'method': 'Get_Langs'
        }
    )
    return Dbl.ExportPair('alias', 'id')
