import os
import json
from psycopg2.extensions import TRANSACTION_STATUS_INERROR
#from aiopg import IsolationLevel, Transaction
#
from Inc.UtilP.Db.DbMeta import TDbMeta
from Inc.UtilP.Db.DbSql import TDbSql
from Inc.Util.Obj import DeepGets

class TModel():
    def __init__(self, aDbMeta: TDbMeta, aPath: str):
        self.DbMeta = aDbMeta
        self.Conf = self._LoadJson(aPath + '/FConf.json')

    def _LoadJson(self, aPath: str) -> dict:
        with open(aPath, 'r', encoding = 'utf8') as F:
            Res = json.load(F)
        return Res

    def _CheckConf(self, aData: dict) -> dict:
        Res = []

        ConfAllow = set(self.Conf.get('allow'))
        Tables = set(aData.keys())
        Diff = Tables - ConfAllow
        if (Diff):
            Res.append(f'unknown {Diff}')

        ConfRequire = self.Conf.get('require', {})
        for Key, Val in ConfRequire.items():
            if (not DeepGets(aData, [Key, Val])):
                Res.append(f'require {Key}:{Val}')
        return Res

    @staticmethod
    def _TransDecor(aFunc):
        async def Wrapper(self, aData, *_aArgs):
            async with self.DbMeta.Db.Pool.acquire() as Connect:
                async with Connect.cursor() as Cursor:
                    Res = {}
                    Trans = await Cursor.begin()

                    Res['func'] = await aFunc(self, aData, Cursor)
                    TransStat = await Connect.get_transaction_status()
                    Res['trans'] = (TransStat != TRANSACTION_STATUS_INERROR)

                    await Trans.commit()
                    return Res
        return Wrapper

    @_TransDecor
    async def Add(self, aData: dict, aCursor = None) -> dict:
        Res = self._CheckConf(aData)
        if (Res):
            return Res

        ConfMaster = self.Conf.get('master', {})
        MasterId = {}
        for Table, Column in ConfMaster.items():
            Dbl = await self.DbMeta.Insert(Table, aData.get(Table, {}), aReturning = [Column], aCursor = aCursor)
            MasterId[Table] = Dbl.Rec.GetField(Column)

        for Table, Data in aData.items():
            if (not Table in ConfMaster):
                Foreign = self.DbMeta.Foreign.FindMaster(Table, ConfMaster, MasterId)
                if (isinstance(Data, list)):
                    for x in Data:
                        await self.DbMeta.Insert(Table, x | Foreign, aCursor = aCursor)
                elif (isinstance(Data, dict)):
                    await self.DbMeta.Insert(Table, Data | Foreign, aCursor = aCursor)
