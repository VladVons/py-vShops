from Inc.UtilP.Db.DbSql import TDbSql
from IncP.Db.Model import TModel
from aiopg import IsolationLevel, Transaction


class TMain(TModel):
    def _GetMasters(self) -> dict:
        return {
            'ref_product0': 'id',
        }
