# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Time import SecondsToDHMS_Str
from Inc.Sql.DbPg import TDbPg
from Inc.WebSrv.WebApi import TApiBase
from IncP.Log import Log, TEchoDb


class TApi(TApiBase):
    def __init__(self):
        super().__init__()

        self.Url = {
            'get_hand_shake':       {'param': []},
            'get_user_id':          {'param': ['login', 'passw']}
        }

        self.Db: TDbPg = None

    async def _DoAuthRequest(self, aUser: str, aPassw: str) -> bool:
        #Dbl = await self.Db.UserAuth(aUser, aPassw)
        #return (not Dbl.IsEmpty())
        return True

    async def path_get_hand_shake(self, _aPath: str, _aData: dict) -> dict:
        return True

    async def path_get_user_id(self, _aPath: str, aData: dict) -> dict:
        Dbl = await self.Db.UserAuth(aData.get('login'), aData.get('passw'))
        return Dbl.Export()

    async def DbInit(self, aAuth: dict):
        self.Db = TDbPg(aAuth)
        await self.Db.Connect()
        # await self.Db.ExecFile('IncP/DB/Scraper_pg.sql')

        Dbl = await self.Db.GetDbVersion()
        Rec = Dbl.Rec
        Version = Rec.GetField('version').split()[:2]
        Uptime = Rec.GetField('uptime')
        Log.Print(1, 'i', 'Server: %s, Uptime: %s, DbName: %s, DbSize: %sM, Tables %s' %
            (
                ' '.join(Version),
                SecondsToDHMS_Str(Uptime.seconds),
                Rec.GetField('db_name'),
                round(Rec.GetField('size') / 1000000, 2),
                Rec.GetField('tables'))
            )

        Log.AddEcho(TEchoDb(self.Db))

    async def DbClose(self):
        List = Log.FindEcho(TEchoDb.__name__)
        Log.Echoes.remove(List[0])
        await self.Db.Close()

Api = TApi()
