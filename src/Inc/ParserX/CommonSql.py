# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
import re
import os
#
from Inc.DbList import TDbList
from Inc.Util.Arr import Parts
from Inc.Log import TLog, TEchoFile


def StripQuery(aData: str) -> str:
    return re.sub(r'\s+', ' ', aData).strip()

def DSplit(aFunc: callable) -> list[str]:
    def Decor(aData: list, aMax: int) -> list[str]:
        Res = []
        for Part in Parts(aData, aMax):
            Data = aFunc(Part, aMax)
            Res.append(StripQuery(Data).strip())
        return Res
    return Decor

def DASplit(aFunc: callable) -> list[str]:
    async def Decor(aData: list, aMax: int) -> list[str]:
        Res = []
        Len = len(aData) // aMax
        for Idx, Part in enumerate(Parts(aData, aMax)):
            Data = await aFunc(Part, aMax, Idx, Len)
            Res.append(Data)
        return Res
    return Decor

def DASplitDbl(aFunc: callable) -> list:
    async def Decor(aDbl: TDbList, aMax: int) -> list:
        Res = []
        Len = aDbl.GetSize() // aMax
        for Idx, Part in enumerate(Parts(aDbl.Data, aMax)):
            Dbl = aDbl.New(Part)
            Data = await aFunc(Dbl, aMax, Idx, Len)
            Res.append(Data)
        return Res
    return Decor


class TLogEx(TLog):
    def Write(self, aData):
        self._Write({'aM': aData}, [])

    def Init(self, aFile: str):
        if (os.path.exists(aFile)):
            os.remove(aFile)
        else:
            os.makedirs(os.path.dirname(aFile), exist_ok=True)

        EchoFile = TEchoFile(aFile)
        EchoFile.Fmt = ['aM']
        return TLogEx([EchoFile])


class TSqlBase():
    def __init__(self):
        self.Now = time.strftime('%Y-%m-%d %H:%M:%S')
        self.Escape = ''.maketrans({
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            "'": '&apos;',
            '"': '&quot;'
            })
