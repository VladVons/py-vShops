import os
import json
from psycopg2.errorcodes import UNIQUE_VIOLATION, NOT_NULL_VIOLATION
from psycopg2 import errors
#
from Inc.UtilP.Db.DbMeta import TDbMeta
from Inc.UtilP.Db.DbSql import TDbSql
from Inc.Util.Obj import DeepGets
from IncP.Log import Log


class TModel():
    def __init__(self, aDbMeta: TDbMeta, aPath: str):
        self.DbMeta = aDbMeta
        self.Conf = self._LoadJson(aPath + '/FConf.json')

    @staticmethod
    def _TransDecor(aFunc):
        async def Wrapper(self, aData, *_aArgs):
            async with self.DbMeta.Db.Pool.acquire() as Connect:
                async with Connect.cursor() as Cursor:
                    Trans = await Cursor.begin()
                    try:
                        Res = await aFunc(self, aData, Cursor)
                    except (
                        errors.lookup(UNIQUE_VIOLATION),
                        errors.lookup(NOT_NULL_VIOLATION)
                    ) as E:
                        Res = {'err': str(E).split('\n', maxsplit = 1)[0]}
                        Log.Print(1, 'x', 'TransDecor()', aE=E, aSkipEcho=['TEchoDb'])

                    if ('err' in Res):
                        #TransStat = await Connect.get_transaction_status()
                        #Res['trans'] = (TransStat != psycopg2.extensions.TRANSACTION_STATUS_INERROR)
                        await Trans.rollback()
                    else:
                        await Trans.commit()
                return Res
        return Wrapper

    def _LoadJson(self, aPath: str) -> dict:
        with open(aPath, 'r', encoding = 'utf8') as F:
            Res = json.load(F)
        return Res

    def _CheckConf(self, aData: dict) -> str:
        def Recurs(aRequire: dict, aData) -> str:
            Res = ''
            if (isinstance(aData, list)):
                for x in aData:
                    Res = Recurs(aRequire, x)
                    if (Res):
                        break
            else:
                Diff = aRequire - set(aData.keys())
                if (Diff):
                    Res = f'required fields {Diff}'
            return Res

        ConfRequire = self.Conf.get('require', [])
        Diff = set(ConfRequire) - set(aData.keys())
        if (Diff):
            return f'require {Diff}'

        ConfMaster = self.Conf.get('master', '')
        ConfAllow = self.Conf.get('allow', [])
        ConfDeny = self.Conf.get('deny', [])
        Depends = self.DbMeta.Foreign.TableId.get((ConfMaster, 'id'))
        for Table, Data in aData.items():
            if (ConfMaster):
                if (Table not in Depends):
                    return f'table {Table} not depends on {ConfMaster}'

            if (ConfAllow) and (Table not in ConfAllow):
                return f'table {Table} not allow'

            if (Table in ConfDeny):
                return f'table {Table} not allow'

            Require = self.DbMeta.Table.Require.get(Table, [])
            Depend = Depends.get(Table)
            if (Depend):
                Require.remove(Depend)
            Res = Recurs(set(Require), Data)
            if (Res):
                return f'table {Table} {Res}'

    @_TransDecor
    async def Add(self, aData: dict, aCursor = None) -> dict:
        Err = self._CheckConf(aData)
        if (Err):
            return {'err': Err}

        ResId = []
        ConfMaster = self.Conf.get('master')
        if (ConfMaster):
            Dbl = await self.DbMeta.Insert(ConfMaster, aData.get(ConfMaster, {}), aReturning = ['id'], aCursor = aCursor)
            ResId = [ConfMaster, Dbl.Rec.GetField('id')]

        for Table, Data in aData.items():
            if (Table not in ConfMaster):
                ForeignVal = self.DbMeta.Foreign.GetColumnVal(Table, ResId)
                if (isinstance(Data, list)):
                    for x in Data:
                        await self.DbMeta.Insert(Table, x | ForeignVal, aCursor = aCursor)
                elif (isinstance(Data, dict)):
                    await self.DbMeta.Insert(Table, Data | ForeignVal, aCursor = aCursor)
        return {'id': ResId}
