# Created: 2022.03.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from datetime import datetime
from urllib.parse import urlparse
import asyncio
import json
#
from Inc.Db.DbList import TDbList, TDbCond
from Inc.Util.Obj import DeepGet
from Inc.UtilP.Time import SecondsToDHMS_Str
from IncP.ApiWeb import TApiBase
from IncP.Db.DbSql import TDbSql
from IncP.DB.Scraper_pg import TDbApp
from IncP.Log import Log, TEchoDb


class TApiTask():
    def __init__(self, aParent: 'TApi'):
        self.Parent = aParent
        self.Tasks = TDbList( [('SiteId', int), ('StartAt', type(datetime.now())), ('Urls', TDbSql)] )
        self.Lock = asyncio.Lock()

    async def Get(self, _aData: dict) -> dict:
        async with self.Lock:
            ExclId = self.Tasks.ExportList('SiteId')

            Dbl = await self.Parent.Db.GetSitesForUpdateFull(aExclId=ExclId, aUpdDaysX=2)
            if (not Dbl.IsEmpty()):
                Dbl.Tag = 'Full'
                Dbl.Shuffle()
                Res = Dbl.Rec.GetAsDict()
                Res['Type'] = Dbl.Tag
                #Res['scheme'] = json.loads(Res['scheme'])
                self.Tasks.RecAdd([Dbl.Rec.GetField('id'), datetime.now(), Dbl])
                return Res

            Dbl = await self.Parent.Db.GetSitesForUpdate(aExclId=ExclId)
            if (not Dbl.IsEmpty()):
                Dbl.Shuffle()
                SiteId = Dbl.Rec.GetField('id')
                Res = Dbl.Rec.GetAsDict()

                Dbl = await self.Parent.Db.GetSiteUrlsForUpdate(SiteId)
                Dbl.Tag = 'Update'
                Res['Type'] = Dbl.Tag
                Res['Urls'] = Dbl.GetData()

                self.Tasks.RecAdd([SiteId, datetime.now(), Dbl])
                return Res


class TApi(TApiBase):
    def __init__(self):
        super().__init__()

        self.Url = {
            'get_hand_shake':       {'param': []},
            'get_task':             {'param': []},
            'get_scheme_empty':     {'param': ['cnt']},
            'get_scheme_not_empty': {'param': ['cnt']},
            'get_scheme_mederate':  {'param': []},
            'get_scheme_by_id':     {'param': ['id']},
            'get_sites':            {'param': ['*']},
            'get_user_id':          {'param': ['login', 'passw']},
            'get_user_rights':      {'param': ['id']},
            'get_user_config':      {'param': ['id']},
            'add_sites':            {'param': ['dbl']},
            'send_result':          {'param': ['*']},
            'set_scheme':           {'param': ['scheme', 'trust']}
        }

        self.TableFields = None
        self.Db: TDbApp = None
        self.ApiTask = TApiTask(self)

    async def DoAuthRequest(self, aUser: str, aPassw: str) -> bool:
        Dbl = await self.Db.UserAuth(aUser, aPassw)
        return (not Dbl.IsEmpty())

    async def path_get_hand_shake(self, _aPath: str, _aData: dict) -> dict:
        return True

    async def path_get_task(self, _aPath: str, aData: dict) -> dict:
        return await self.ApiTask.Get(aData)

    async def path_get_scheme_empty(self, _aPath: str, aData: dict) -> dict:
        Dbl = await self.Db.GetScheme(True, aData.get('cnt', 1))
        return Dbl.Export()

    async def path_get_scheme_not_empty(self, _aPath: str, aData: dict) -> dict:
        Dbl = await self.Db.GetScheme(False, aData.get('cnt', 1))
        return Dbl.Export()

    async def path_get_scheme_mederate(self, _aPath: str, _aData: dict) -> dict:
        Dbl = await self.Db.GetSchemeModerate()
        return Dbl.Export()

    async def path_get_scheme_by_id(self, _aPath: str, aData: dict) -> dict:
        Dbl = await self.Db.GetSiteById(aData.get('id'))
        return Dbl.Export()

    async def path_set_scheme(self, _aPath: str, aData: dict) -> dict:
        Scheme = json.loads(aData.get('scheme'))
        Urls = DeepGet(Scheme, 'Product.Info.Url')
        if (Urls):
            UrlInf = urlparse(Urls[0])
            Url = UrlInf.scheme + '://' + UrlInf.hostname
            return await self.Db.SetScheme(Url, aData.get('scheme'), aData.get('trust', False))

    async def path_get_sites(self, _aPath: str, aData: dict) -> dict:
        Dbl = await self.Db.GetSites(aData.get('cnt', -1))
        return Dbl.Export()

    async def path_get_user_id(self, _aPath: str, aData: dict) -> dict:
        Dbl = await self.Db.UserAuth(aData.get('login'), aData.get('passw'))
        return Dbl.Export()

    async def path_get_user_config(self, _aPath: str, aData: dict) -> dict:
        Conf = {}

        UserId = aData.get('id')
        Dbl = await self.Db.GetUserInfo(UserId)
        if (not Dbl.IsEmpty()):
            GroupId = Dbl.Rec.GetField('auth_group_id')
            if (GroupId):
                Dbl = await self.Db.GetGroupConf(GroupId)
                Conf = Dbl.ExportPair('name', 'data')

            Dbl = await self.Db.GetUserConf(UserId)
            if (not Dbl.IsEmpty()):
                Data = Dbl.ExportPair('name', 'data')
                if (Data):
                    Conf.update(Data)
        Dbl = TDbList().ImportPair(Conf, 'name', ('data', str))
        return Dbl.Export()

    async def path_add_sites(self, _aPath: str, aData: dict) -> dict:
        Data = aData.get('dbl')
        Dbl = TDbSql(self.Db).Import(Data)
        await Dbl.Insert('site')
        return True

    async def path_send_result(self, _aPath: str, aData: dict) -> dict:
        Dbl = TDbList().Import(aData)
        DblFields = Dbl.Fields.GetList()

        TableFields = self.TableFields['url']
        Fields = [x for x in DblFields if (x in TableFields)]
        DblS = TDbSql(self.Db).ImportDbl(Dbl, Fields)
        IDs = await DblS.InsertUpdate('url', 'url')

        TableFields = self.TableFields['product']
        Fields = [x for x in DblFields if (x in TableFields)]
        DblS = TDbSql(self.Db).ImportDbl(Dbl, Fields)

        DblS.AddField([('url_id', int)])
        for Idx, Rec in enumerate(DblS):
            Id = IDs[0][Idx][0]
            Rec.SetField('url_id', Id)
            Rec.Flush()

        Cond = TDbCond().AddFields([
            ['ne', (DblS, 'name'), '', True]
        ])
        DblS = TDbSql(self.Db).ImportDbl(DblS, aCond=Cond)
        if (not DblS.IsEmpty()):
            await DblS.Insert('product')

        return True

    async def DbInit(self, aAuth: dict):
        self.Db = TDbApp(aAuth)
        await self.Db.Connect()
        # await self.Db.ExecFile('IncP/DB/Scraper_pg.sql')

        self.TableFields = await self.Db.GetTablesColumns(['url', 'product'])

        Dbl = await self.Db.GetDbVersion()
        Rec = Dbl.Rec
        Version = Rec.GetField('version').split()[:2]
        Uptime = Rec.GetField('uptime')
        Log.Print(1, 'i', 'Server: %s, Uptime: %s, DbName: %s, DbSize: %sM, Tables %s' %
            (' '.join(Version), SecondsToDHMS_Str(Uptime.seconds), Rec.GetField('name'), round(Rec.GetField('size') / 1000000, 2), Rec.GetField('tables'))
        )

        Log.AddEcho(TEchoDb(self.Db))

    async def DbClose(self):
        List = Log.FindEcho(TEchoDb.__name__)
        Log.Echoes.remove(List[0])
        await self.Db.Close()


Api = TApi()
