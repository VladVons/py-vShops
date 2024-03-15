# Created: 2023.03.12
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


# pylint: skip-file
from Inc.DbList import TDbList, TDbSql, TDbRec
from Inc.Misc.Image import TImage
from Inc.Misc.Pagination import TPagination
from Inc.Misc.Request import TDownload, TDownloadImage
from Inc.Util.Str import UrlUdate, Replace
from Inc.Util.Obj import DeepGetByList, GetDictDef, GetDictDefs, Filter, DeepGetsRe, Iif, IsDigits

from .Log import Log

def ResGetModule(aData: dict, aName: str) -> dict:
    for x in aData['res']['modules']:
        if (x['layout']['code'] == aName):
            return x
    return {}

def ResGetLang(aData: dict, aName: str) -> dict:
    return aData['res']['lang'].get(aName, '')

def AttrDecode(aVal: str) -> dict:
    Res = {}
    if (aVal):
        for Group in aVal.strip('[]').split(';;'):
            if (Group):
                Pair = Group.split(':')
                if (len(Pair) == 2):
                    AttrId, Val = Pair
                    if (AttrId.isdigit()):
                        Res[AttrId] = Val.split(';')
    return Res
