# Created: 2023.05.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
#PluginEan = TPluginEan('IncP/PluginEan')
#Parser = PluginEan.Load('listex_info')
#await Parser.Init()
#Data = await Parser.GetData('4823003207513')


import re
import os
import json
import asyncio
from aiohttp import ClientConnectorError
from bs4 import BeautifulSoup
#
from Inc.Ean import TEan
from Inc.Scheme.Scheme import TSoupScheme
from Inc.Util.Mod import DynImport
from Inc.Util.Obj import DeepGetByList
from IncP.Log import Log


class TParserBase():
    CodeAllow = '.*'
    CodeType = 'ean'
    Headers = {}
    ImageNeed = True
    Moderate = True
    SkipFeatures = {}
    UrlRoot = ''

    async def _GetData(self, aCode: str) -> dict:
        raise NotImplementedError()

    async def Init(self):
        pass

    @staticmethod
    def _WriteFile(aFile: str, aData, aMod = 'w'):
        if (isinstance(aData, dict)):
            aData = json.dumps(aData, indent=2, ensure_ascii=False)
        elif (isinstance(aData, bytes)) and (aMod != 'wb'):
            aData = aData.decode('utf-8')

        with open(aFile, aMod) as F:
            F.write(aData)

    @staticmethod
    def _DictToCookie(aDict) -> str:
        return '; '.join([f'{Key}={Val}' for Key, Val in aDict.items()])

    async def GetData(self, aCode: str) -> dict:
        try:
            return await self._GetData(aCode)
        except ClientConnectorError as E:
            Log.Print(1, 'x', f'GetData({aCode})', aE = E)
            await asyncio.sleep(3)

    def CheckEan(self, aCode: str) -> bool:
        Res = False
        if (aCode.startswith('02')):
            Log.Print(1, 'i', f'EAN internal {aCode}')
        elif (not re.match(self.CodeAllow, aCode)):
            Log.Print(1, 'i', f'EAN filter {aCode}')
        elif (not TEan(aCode).Check()):
            Log.Print(1, 'i', f'EAN error {aCode}')
        else:
            Res = True
        return Res

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


class TPluginEan():
    def __init__(self, aDir: str):
        self.Dir = aDir

    def Load(self, aParser: str) -> TParserBase:
        Module = f"{self.Dir.replace('/', '.')}.{aParser}"
        TClass, Err = DynImport(Module, 'TParser')
        assert(not Err), f'{Err}'

        return TClass()
