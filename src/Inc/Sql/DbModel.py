# Created: 2022.02.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
#
from IncP.Log import Log
from Inc.DbList import TDbSql
from Inc.Loader.Query import TLoaderQueryFs
from . import TDbExecCursor, TDbExecPool, DTransaction


class TDbModel():
    def __init__(self, aApi: 'TApiModel', aPath: str):
        self.ApiModel = aApi
        self.DbMeta = aApi.DbMeta
        self.Db = aApi.DbMeta.Db # for DTransaction decorator
        self.Conf = self._LoadJson(aPath + '/FConf.json')
        self.Master = self.Conf.get('master', '')

        #self.Query = TQueryDb(self, aApi.DbMeta.Db)
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
            Dbl = await TDbExecCursor(aCursor).Exec(Query)
            ResId = [self.Master, Dbl.Rec.id]

        for TableK, DataV in aData.items():
            if (TableK not in self.Master):
                DblIn.Import(DataV)
                ForeignVal = self.DbMeta.Foreign.GetColumnVal(TableK, ResId)
                if (ForeignVal):
                    DblIn.AddFields(ForeignVal.keys(), ForeignVal.values())
                Query = DblIn.GetSqlInsert(TableK)
                await TDbExecCursor(aCursor).Exec(Query)
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
        Dbl = await TDbExecCursor(aCursor).Exec(Query)
        #Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
        return (Dbl.Rec.count > 0)

    async def ExecQueryText(self, aQuery: str) -> TDbSql:
        Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(aQuery)
        if (Dbl is not None):
            return Dbl.Export()

    async def ExecQueryTextCursor(self, aQuery: str, aCursor) -> TDbSql:
        Dbl = await TDbExecCursor(aCursor).Exec(aQuery)
        if (Dbl):
            return Dbl.Export()

    async def ExecQuery(self, aPath: str, aValues: dict = None) -> tuple:
        aValues = aValues or {}
        Query = await self.Query.Get(aPath, aValues)
        #print('debug--\n', Query)
        #Log.Print(1, 'i', f'ExecQuery({self.Query.Path}/{aPath}, {aValues})')
        try:
            Res = await self.ExecQueryText(Query)
        except Exception as E:
            Log.Print(1, 'e', Query, aE = E)
            raise
        return Res

    async def ExecQueryCursor(self, aPath: str, aValues: dict, aCursor) -> tuple:
        Query = await self.Query.Get(aPath, aValues)
        try:
            Res = await self.ExecQueryTextCursor(Query, aCursor)
        except Exception as E:
            Log.Print(1, 'e', Query, aE = E)
            raise
        return Res
