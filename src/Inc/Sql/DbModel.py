# Created: 2022.02.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
#
from psycopg2.errorcodes import (
    UNIQUE_VIOLATION,
    NOT_NULL_VIOLATION,
    UNDEFINED_COLUMN,
    FOREIGN_KEY_VIOLATION,
    SYNTAX_ERROR
)
from psycopg2 import errors
#
from IncP.Log import Log
from Inc.DbList import TDbSql
from Inc.Loader.Query import TLoaderQueryFs
from .DbMeta import TDbMeta
from .ADb import TDbExecCurs, TDbExecPool


def DTransaction(aFunc):
    async def Decor(self, aData, *_aArgs):
        async with self.DbMeta.Db.Pool.acquire() as Connect:
            async with Connect.cursor() as Cursor:
                Trans = await Cursor.begin()
                try:
                    Res = await aFunc(self, aData, Cursor)
                except (
                    errors.lookup(UNIQUE_VIOLATION),
                    errors.lookup(NOT_NULL_VIOLATION),
                    errors.lookup(UNDEFINED_COLUMN),
                    errors.lookup(FOREIGN_KEY_VIOLATION),
                    errors.lookup(SYNTAX_ERROR)
                ) as E:
                    Res = {'err': str(E).split('\n', maxsplit = 1)[0]}
                    Log.Print(1, 'x', 'DTransaction()', aE=E, aSkipEcho=['TEchoDb'])

                if (Res) and ('err' in Res):
                    #TransStat = await Connect.get_transaction_status()
                    #Res['trans'] = (TransStat != psycopg2.extensions.TRANSACTION_STATUS_INERROR)
                    await Trans.rollback()
                else:
                    await Trans.commit()
            return Res
    return Decor


class TDbModel():
    def __init__(self, aDbMeta: TDbMeta, aPath: str):
        self.DbMeta = aDbMeta
        self.Conf = self._LoadJson(aPath + '/FConf.json')
        self.Master = self.Conf.get('master', '')

        #self.Query = TQueryDb(self, aDbMeta.Db)
        self.Query = TLoaderQueryFs(self)

    def _LoadJson(self, aPath: str) -> dict:
        Res = {}
        if (os.path.exists(aPath)):
            with open(aPath, 'r', encoding = 'utf8') as F:
                Res = json.load(F)
        return Res

    def _CheckData(self, aData: dict) -> list[str]:
        ResErr = []

        ConfRequire = self.Conf.get('require', [])
        Diff = set(ConfRequire) - set(aData.keys())
        if (Diff):
            ResErr.append(f'require {Diff}')

        ConfAllow = self.Conf.get('allow', [])
        ConfDeny = self.Conf.get('deny', [])
        Depends = self.DbMeta.Foreign.TableId.get((self.Master, 'id'), {})

        for Table, Data in aData.items():
            if (self.Master):
                if (Table == self.Master):
                    if (len(Data.get('data', [])) > 1):
                        ResErr.append(f'{Table} rows must be 1')
                else:
                    if (Depends) and (Table not in Depends):
                        ResErr.append(f'{Table} not depends on {self.Master}')

            if (ConfAllow) and (Table not in ConfAllow):
                ResErr.append(f'{Table} is not allowed')

            if (Table in ConfDeny):
                ResErr.append(f'{Table} denied')
        return ResErr

    async def _Add(self, aData: dict, aCursor = None) -> dict:
        Err = self._CheckData(aData)
        if (Err):
            return {'err': ', '.join(Err)}

        ResId = []
        DblIn = TDbSql()
        if (self.Master):
            DblIn.Import(aData.get(self.Master))
            Query = DblIn.GetSqlInsert(self.Master, ['id'])
            Dbl = await TDbExecCurs(aCursor).Exec(Query)
            ResId = [self.Master, Dbl.Rec.id]

        for TableK, DataV in aData.items():
            if (TableK not in self.Master):
                DblIn.Import(DataV)
                ForeignVal = self.DbMeta.Foreign.GetColumnVal(TableK, ResId)
                if (ForeignVal):
                    DblIn.AddFields(ForeignVal.keys(), ForeignVal.values())
                Query = DblIn.GetSqlInsert(TableK)
                await TDbExecCurs(aCursor).Exec(Query)
        return {'id': ResId}

    async def _Del(self, aId: int, aCursor = None) -> dict:
        if (not await self.MasterHasId(aId, aCursor)):
            return {'err': f'id {aId} not found'}

        Depends = self.DbMeta.Foreign.TableId.get((self.Master, 'id'), {})
        for Table, Column in Depends.items():
            if ('_table_' not in Table):
                await self.DbMeta.Delete(Table, f'{Column} = {aId}', aCursor)
        await self.DbMeta.Delete(self.Master, f'id = {aId}', aCursor)

    @DTransaction
    async def _AddTD(self, aData: dict, aCursor = None) -> dict:
        return await self._Add(aData, aCursor)

    @DTransaction
    async def _AddListTD(self, aData: list, aCursor = None) -> list:
        Res = []
        for xData in aData:
            ResF = await self._Add(xData, aCursor)
            Res.append(ResF)
        return Res

    @DTransaction
    async def _DelTD(self, aId: int, aCursor = None) -> dict:
        return await self._Del(aId, aCursor)

    @DTransaction
    async def _DelListTD(self, aId: list[int], aCursor = None) -> list:
        Res = []
        for xId in aId:
            ResF = await self._Del(xId, aCursor)
            Res.append(ResF)
        return Res

    async def Add(self, aData: dict) -> dict:
        return await self._AddTD(aData)

    async def AddList(self, aData: list) -> list:
        return await self._AddListTD(aData)

    async def Del(self, aId: int) -> dict:
        return await self._DelTD(aId)

    async def DelList(self, aId: list[int]) -> list:
        return await self._DelListTD(aId)

    async def MasterHasId(self, aId: int, aCursor) -> bool:
        Query = f'''
            select
                count(*) as count
                from
                    {self.Master}
                where
                    id = {aId}
        '''
        Dbl = await TDbExecCurs(aCursor).Exec(Query)
        #Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
        return (Dbl.Rec.count > 0)

    async def ExecQueryText(self, aQuery: str) -> TDbSql:
        Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(aQuery)
        if (Dbl):
            return Dbl.Export()

    async def ExecQuery(self, aPath: str, aValues: dict) -> TDbSql:
        Query = await self.Query.Get(aPath, aValues)
        return await self.ExecQueryText(Query)
