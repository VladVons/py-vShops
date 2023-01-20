from Inc.UtilP.Db.DbSql import TDbSql
from Inc.UtilP.Db.DbModel import TDbModel


class TMain():
    def __init__(self):
        self.Db = None

    async def Add(self, aData: dict):
        Query = '''
            insert into ref_product0
            default values
            returning id
        '''
        Fetch = await TDbSql(self.Db).Fetch(Query)

        pass
