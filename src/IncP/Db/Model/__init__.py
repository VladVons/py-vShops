from psycopg2.extensions import TRANSACTION_STATUS_INERROR
#from aiopg import IsolationLevel, Transaction
#
from Inc.UtilP.Db.DbMeta import TDbMeta
from Inc.UtilP.Db.DbSql import TDbSql


class TModel():
    DbMeta: TDbMeta = None

    def _GetMasters(self) -> dict:
        raise NotImplementedError()

    @staticmethod
    def TransDecor(aFunc):
        async def Wrapper(self, aData, *_aArgs):
            async with self.DbMeta.Db.Pool.acquire() as Connect:
                async with Connect.cursor() as Cursor:
                    Trans = await Cursor.begin()
                    ResFunc = await aFunc(self, aData, Cursor)
                    ResTrans = await Connect.get_transaction_status()
                    await Trans.commit()
                    return (ResTrans != TRANSACTION_STATUS_INERROR) and ResFunc
        return Wrapper

    def FindForeign(self, aTable: str, aMasters: dict, aMasterId: dict):
        Res = {}
        Data = self.DbMeta.Foreign.get(aTable, {})
        for Key, Val in Data.items():
            if (Val[0] in aMasters):
                Res = {Key: aMasterId.get(Val[0])}
        return Res

    @TransDecor
    async def Add(self, aData: dict, aCursor = None):
        Masters = self._GetMasters()
        MasterId = {}
        for Table, Column in Masters.items():
            Dbl = await self.DbMeta.Insert(Table, aData[Table], aReturning = [Column], aCursor = aCursor)
            MasterId[Table] = Dbl.Rec.GetField(Column)

        for Table, Data in aData.items():
            if (not Table in Masters):
                Foreign = self.FindForeign(Table, Masters, MasterId)
                if (isinstance(Data, list)):
                    for x in Data:
                        await self.DbMeta.Insert(Table, x | Foreign, aCursor = aCursor)
                elif (isinstance(Data, dict)):
                    await self.DbMeta.Insert(Table, Data | Foreign, aCursor = aCursor)
        return True
