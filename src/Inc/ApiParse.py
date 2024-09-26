# Created: 2021.02.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# micropython ESP8266


import json
#
from Inc.Util import FS
from Inc.Var import Str


def QueryToDict(aQuery: str) -> dict:
    R = {}
    for Item in aQuery.split('&'):
        if (Item):
            Key, Value = Str.SplitPad(2, Item, '=')
            R[Key] = Value
    return R

# simplify QueryUrl + GetApi to avoid `too many recursuin`
async def QueryUrl(aPath: str, aQuery: dict) -> str:
    DirCore = 'IncP/Api'
    DirUser = 'Plugin/Api'

    Name, Ext = Str.SplitPad(2, aPath.split('/')[-1], '.')
    if (Ext == 'py'):
        if (FS.FileExists(DirUser + aPath)):
            Dir = DirUser
        else:
            Dir = DirCore
        Lib = __import__(Dir + '/' + Name)
        R = await Lib.TApi().Query(aQuery)
        return json.dumps(R) + '\r\n'
