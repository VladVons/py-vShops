from psycopg2.extensions import TRANSACTION_STATUS_INERROR
#from aiopg import IsolationLevel, Transaction
#
from Inc.UtilP.Db.DbMeta import TDbMeta
from Inc.UtilP.Db.DbSql import TDbSql


class TModel():
    DbMeta: TDbMeta = None

    def _GetConf(self) -> dict:
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
                    return (ResTrans != TRANSACTION_STATUS_INERROR, ResFunc)
        return Wrapper

    @TransDecor
    async def Add(self, aData: dict, aCursor = None):
        Conf = self._GetConf()
        ConfMasters = Conf.get('masters', {})
        ConfParam = Conf.get('param', {})

        MasterId = {}
        for Table, Column in ConfMasters.items():
            Dbl = await self.DbMeta.Insert(Table, aData[Table], aReturning = [Column], aCursor = aCursor)
            MasterId[Table] = Dbl.Rec.GetField(Column)

        for Table, Data in aData.items():
            if (not Table in ConfMasters):
                Foreign = self.DbMeta.Foreign.Find(Table, ConfMasters, MasterId)
                if (isinstance(Data, list)):
                    for x in Data:
                        await self.DbMeta.Insert(Table, x | Foreign, aCursor = aCursor)
                elif (isinstance(Data, dict)):
                    await self.DbMeta.Insert(Table, Data | Foreign, aCursor = aCursor)
