# Created: 2023.12.21
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


# pylint: skip-file
from Inc.DbList import TDbSql
#from Inc.Util.Obj import DeepGetByList, GetDictDef, GetDictDefs
from Inc.Sql.DbModel import DTransaction, TDbExecCursor

from .Log import Log


def DictToComma(aData: dict) -> str:
    Res = []
    for Key, Val in aData.items():
        if (isinstance(Val, str)):
            Val = f"'{Val}'"
        Res.append(f'{Key} = {Val}')
    return ', '.join(Res)
