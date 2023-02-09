import json
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

    def _LoadJson(self, aPath: str) -> dict:
        with open(aPath, 'r', encoding = 'utf8') as F:
            Res = json.load(F)
        return Res

    def _CheckData(self, aData: dict) -> list[str]:
        ResErr = []
        ResNomad = {}

        ConfRequire = self.Conf.get('require', [])
        Diff = set(ConfRequire) - set(aData.keys())
        if (Diff):
            ResErr.append(f'require {Diff}')

        ConfAllow = self.Conf.get('allow', [])
        ConfDeny = self.Conf.get('deny', [])
        Depends = self.DbMeta.Foreign.TableId.get((self.Master, 'id'), {})

        if (self.Master) and (self.Master not in aData):
            aData[self.Master] = [{}]

        for Table, Data in aData.items():
            if (self.Master):
                if (Table == self.Master):
                    if (len(Data) > 1):
                        ResErr.append(f'{Table} rows must be 1')
                else:
                    if (Depends) and (Table not in Depends):
                        ResErr.append(f'{Table} not depends on {self.Master}')

            if (ConfAllow) and (Table not in ConfAllow):
                ResErr.append(f'{Table} is not allowed')

            if (Table in ConfDeny):
                ResErr.append(f'{Table} denied')

            Columns = set(self.DbMeta.Table.Column.get(Table, []))
            Require = set(self.DbMeta.Table.Require.get(Table, []))
            Depend = Depends.get(Table)
            if (Depend):
                Require.remove(Depend)

            NomadCnt = {}
            for xData in Data:
                for x in xData:
                    NomadCnt[x] = NomadCnt.get(x, 0) + 1

                RowColumns = set(xData.keys())
                Diff = Require - RowColumns
                if (Diff):
                    ResErr.append(f'{Table} requires fields {Diff}')

                Diff = RowColumns - Columns
                if (Diff):
                    ResErr.append(f'{Table} unknown columns {Diff}')
            ResNomad[Table] = [Key for Key, Val in NomadCnt.items() if (Val != len(Data))]
        return {'err': ResErr, 'nomad': ResNomad}

    async def _Add(self, aData: dict, aCursor = None) -> dict:
        DataF = self._CheckData(aData)
        if ('err' in DataF):
            return {'err': ', '.join(DataF['err'])}

        ResId = []
        if (self.Master):
            Dbl = await self.DbMeta.Insert(self.Master, aData.get(self.Master)[0], aReturning = ['id'], aCursor = aCursor)
            ResId = [self.Master, Dbl.Rec.GetField('id')]

        for TableK, DataV in aData.items():
            if (TableK not in self.Master):
                ForeignVal = self.DbMeta.Foreign.GetColumnVal(TableK, ResId)
                for x in DataV:
                    x.update(ForeignVal)
                await self.DbMeta.Insert(TableK, DataV, aCursor = aCursor)
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
        Query = f'select count(*) as count from {self.Master} where id = {aId}'
        Dbl = await TDbExecCurs(aCursor).Exec(Query)
        #Dbl = await TDbExecPool(self.DbMeta.Db.Pool).Exec(Query)
        return Dbl.Rec.GetField('count') > 0
