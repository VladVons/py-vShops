# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from bs4 import BeautifulSoup
import lxml
#
from Inc.DataClass import DDataClass
from Inc.DbList  import TDbList, TDbRec
from Inc.Misc.Request import TRequestJson, TRequestGet, TAuth
from Inc.ParserX.Common import TFileBase
from Inc.ParserX.CommonSql import TSqlBase, DASplit, TLogEx
from Inc.Scheme.Scheme import TScheme
from Inc.Sql.ADb import TDbExecPool
from Inc.Sql.DbPg import TDbPg
from Inc.Util.Obj import DeepGetByList
from IncP.Log import Log
from ..CommonDb import TDbCrawl


def GetSoup(aData: str) -> BeautifulSoup:
    #Res = BeautifulSoup(aData, 'lxml')
    Res = BeautifulSoup(aData, lxml.__name__)
    if (len(Res) == 0):
        Res = BeautifulSoup(aData, 'html.parser')
    return Res

@DDataClass
class TSqlConf():
    LangId: int
    SchemeUrl: str
    MaxDays: int = 30
    Parts: int = 100

class TSql(TSqlBase):
    def __init__(self, aDb: TDbPg, aSqlConf: TSqlConf, aImgApi: TRequestJson):
        super().__init__()

        self.Db = aDb
        self.Conf = aSqlConf
        self.ImgApi = aImgApi
        self.ConfCrawl: TDbList

    async def GetConfCrawl(self) -> TDbList:
        Query = f'''
            select
                scheme, max_days
            from
                ref_crawl_site rcs
            where
                (enabled) and (url = '{self.Conf.SchemeUrl}')
        '''
        return await TDbExecPool(self.Db.Pool).Exec(Query)

    async def Parse(self, aEan: str):
        Data = self.ConfCrawl.Rec.scheme[0]
        Pattern = DeepGetByList(Data, ['Product', 'Info', 'Pattern'])
        Url = Pattern % (aEan)

        Request = TRequestGet()
        Data = await Request.Send(Url)
        if ('err' not in Data):
            Soup = GetSoup(Data['data'])
            Scheme = TScheme(self.ConfCrawl.Rec.scheme[0])
            Scheme.Parse(Soup)
            pass

    async def Product0_Create(self, aDbl: TDbCrawl):
        @DASplit
        async def SProduct0(aData: list, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            nonlocal DbRec
            print('SProduct0()', aIdx, aLen)

            Values = [f"('{DbRec.ean}')" for DbRec.Data in aData]
            Query = f'''
                select
                    t2.code
                from (
                    values {', '.join(Values)}
                ) as t2 (code)
                left join ref_product0_barcode rpb on
                    (t2.code = rpb.code) and (rpb.product_en = 'ean')
                left join ref_product0_crawl rpc on
                    (t2.code = rpc.code) and (rpc.product_en = 'ean') and
                    (rpc.info is null) and (DATE_PART('day', now() - rpc.update_date) > {self.Conf.MaxDays})
                where
                    (rpb.code is null) and (rpc.url is null)
            '''
            DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)

            for Rec in DblCur:
                await self.Parse(Rec.code)

        DbRec = TDbRec()
        DbRec.Fields = aDbl.Rec.Fields

        self.ConfCrawl = await self.GetConfCrawl()

        Log.Print(1, 'i', 'Product0')
        await SProduct0(aDbl.Data, self.Conf.Parts)


class TMain(TFileBase):
    def __init__(self, aParent, aDb: TDbPg):
        super().__init__(aParent)

        ConfFile = self.Parent.GetFile()
        self.LogEx = TLogEx()
        self.LogEx = self.LogEx.Init(ConfFile)

        SqlDef = self.Parent.Conf.GetKey('sql', {})
        SqlConf = TSqlConf(
            LangId = SqlDef.get('lang_id'),
            SchemeUrl = SqlDef.get('scheme_url'),
            Parts = SqlDef.get('parts', 50)
        )

        ConfImg = self.Parent.Conf.GetKey('img_loader')
        ImgApi = TRequestJson(aAuth=TAuth(ConfImg.get('user'), ConfImg.get('password')))
        ImgApi.Url = ConfImg.get('url')

        self.Sql = TSql(aDb, SqlConf, ImgApi)


    async def InsertToDb(self, aDbCrawl: TDbCrawl):
        await self.Sql.Product0_Create(aDbCrawl)
