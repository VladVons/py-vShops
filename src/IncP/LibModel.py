# Created: 2023.12.21
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


# pylint: skip-file
from Inc.DbList import TDbList
from Inc.Util.Dict import DeepGetByList, GetDictDef, GetDictDefs
from Inc.Util.DictEx import DeepGetsRe
from Inc.Sql import DTransaction, TDbExecCursor, ListToComma, ListIntToComma, DictToComma, TDbSql
from .Log import Log


def Escape(aVal: str) -> str:
    return aVal.replace("'", "''")
