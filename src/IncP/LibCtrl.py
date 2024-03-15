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

def FindModule(aData: dict, aName: str) -> dict:
    for x in aData['res']['modules']:
        if (x['layout']['code'] == aName):
            return x

def FindLang(aData: dict, aName: str) -> dict:
    return aData['res']['lang'].get(aName, '')
