# Created: 2023.05.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
#PluginEan = TPluginEan('IncP/PluginEan')
#PluginEan.Load('listex_info')
#Data = await PluginEan.GetData('4823003207513')


import os
import json
from bs4 import BeautifulSoup
#
from Inc.Scheme.Scheme import TSoupScheme
from Inc.Util.Mod import DynImport
from Inc.Util.Obj import DeepGetByList


class TParserBase():
    UrlRoot = ''
    EanAllow = '.*'
    Moderate = False

    async def _GetData(self, aEan: str) -> dict:
        raise NotImplementedError()

    async def _Init(self):
        pass

    @staticmethod
    def _WriteFile(aFile: str, aData, aMod = 'w'):
        if (isinstance(aData, dict)):
            aData = json.dumps(aData, indent=2, ensure_ascii=False)

        with open(aFile, aMod) as F:
            F.write(aData)

    @staticmethod
    def _DictToCookie(aDict) -> str:
        return '; '.join([f'{Key}={Val}' for Key, Val in aDict.items()])

    def ParseScheme(self, aData: str, aFile: str = 'scheme.json') -> dict:
        Res = {}
        File = '%s/%s' % (self.__class__.__module__.replace('.', '/'), aFile)
        if (os.path.isfile(File)):
            with open(File, 'rb') as F:
                Scheme = json.load(F)

            Soup = BeautifulSoup(aData, 'lxml')
            SoupScheme = TSoupScheme()
            ResParse = SoupScheme.Parse(Soup, Scheme)
            Res['data'] = DeepGetByList(ResParse, ['product', 'pipe'])
            if (SoupScheme.Err):
                Res['err'] = SoupScheme.Err
        return Res

    async def GetData(self, aEan: str) -> dict:
        await self._Init()
        return await self._GetData(aEan)


class TPluginEan():
    def __init__(self, aDir: str):
        self.Dir = aDir
        self.Parser: TParserBase = None

    def Load(self, aParser: str) -> TParserBase:
        Module = f"{self.Dir.replace('/', '.')}.{aParser}"
        TClass, Err = DynImport(Module, 'TParser')
        assert(not Err), f'{Err}'

        self.Parser = TClass()
        return self.Parser

    async def GetData(self, aCode: str) -> dict:
        return await self.Parser.GetData(aCode)
