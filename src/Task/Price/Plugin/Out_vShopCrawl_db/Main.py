# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
# 4823096802060 long name


import json
import asyncio
import hashlib
from bs4 import BeautifulSoup
import lxml
#
from Inc.DataClass import DDataClass
from Inc.DbList  import TDbList
from Inc.Ean import TEan
from Inc.Misc.Request import TRequestJson, TRequestGet, TAuth
from Inc.ParserX.Common import TFileBase
from Inc.ParserX.CommonSql import TSqlBase, DASplitDbl, TLogEx
from Inc.Scheme.Scheme import TSoupScheme
from Inc.Sql import TDbExecPool, TDbPg, ListToComma
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
    MaxConn: int = 1


class TSql(TSqlBase):
    def __init__(self, aDb: TDbPg, aSqlConf: TSqlConf, aImgApi: TRequestJson):
        super().__init__()

        self.Db = aDb
        self.Conf = aSqlConf
        self.ImgApi = aImgApi
        self.ConfCrawl: TDbList
        self.Parser = None

    async def GetConfCrawl(self) -> TDbList:
        Query = f'''
            select
                id, scheme, max_days
            from
                ref_crawl_site rcs
            where
                (enabled) and (url = '{self.Conf.SchemeUrl}')
        '''
        return await TDbExecPool(self.Db.Pool).Exec(Query)

    async def _ImgUpdate(self, aData):
        Url = f'{self.ImgApi.Url}/system'
        return await self.ImgApi.Send(Url, aData)

    async def _Parse_ListexInfo(self, aEan: str) -> dict:
        Scheme = self.ConfCrawl.Rec.scheme
        Pattern = DeepGetByList(Scheme[0], ['product', 'info', 'pattern'])

        Res = {'url': Pattern % (aEan)}
        Request = TRequestGet()
        Data = await Request.Send(Res['url'])
        if ('err' not in Data):
            Soup = GetSoup(Data['data'])
            SoupScheme = TSoupScheme()
            ResParse = SoupScheme.Parse(Soup, Scheme[0])
            if (not SoupScheme.Err):
                Url = DeepGetByList(ResParse, ['product', 'pipe', 'product'])
                Data = await Request.Send(Url)
                if ('err' not in Data):
                    Soup = GetSoup(Data['data'])
                    SoupScheme = TSoupScheme()
                    ResParse = SoupScheme.Parse(Soup, Scheme[1])
                    Images = DeepGetByList(ResParse, ['product', 'pipe', 'images'])
                    if (Images):
                        Res['data'] = ResParse
        await Request.Close()
        return Res

    async def EanNullInfo(self):
        Query = '''
            select code
            from ref_product0_crawl rpc
            where (product_en = 'ean') and (info is null)
        '''
        return await TDbExecPool(self.Db.Pool).Exec(Query)

    async def EanPotentialFind(self, aDbl: TDbList):
        Dbl = await self.EanNullInfo()
        Pairs = Dbl.ExportPair('code', 1)
        Res = [Rec.ean for Rec in aDbl if Rec.ean in Pairs]
        print(f'Need ean: {len(Dbl)}, records in file: {len(aDbl)}, matches: {len(Res)}')

    async def EanRemoveBad(self):
        DblCur = await self.EanNullInfo()

        EanCrc = TEan()
        Eans = []
        for Rec in DblCur:
            Ean = Rec.code.strip()
            if (len(Ean) < 8) or (Ean.startswith('02')) or (not EanCrc.Init(Ean).Check()):
                Eans.append(Ean)

        Query = f'''
            delete
            from ref_product0_crawl
            where (product_en = 'ean') and (code in ({ListToComma(Eans)}))
        '''
        DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)

    async def Product0_Create(self, aDbl: TDbCrawl):
        async def ReportCrawl():
            Query = '''
                select
                    count(*) as ean_all,
                    count(info) as ean_yes,
                    count(case when info is null then 1 end) as ean_no
                from
                    ref_product0_crawl rpc
            '''
            DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)
            Log.Print(1, 'i', f'ReportCrawl(), {DblCur.Rec.GetAsDict()}')

        async def UpdateCrawl(aEan: str, aUrl: str, aInfo: dict):
            if (aInfo):
                Info = "'" + json.dumps(aInfo, ensure_ascii=False).replace("'", '`') + "'"
            else:
                Info = 'null'

            Query = f'''
                insert into ref_product0_crawl (code, product_en, url, update_date, info, crawl_site_id)
                values ('{aEan}', 'ean', '{aUrl}', now(), {Info}, {self.ConfCrawl.Rec.id})
                on conflict (code, product_en) do update
                set update_date = now(), info = {Info}
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

        async def UpdateImage(aEan: str, aInfo: dict) -> list:
            Images = aInfo.get('images', [])

            Query = f'''
                select src_url, src_size
                from ref_product0_image
                where (src_url in ({ListToComma(Images)}))
            '''
            DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)
            UrlSize = DblCur.ExportPair('src_url', 'src_size')

            UrlD = []
            for Idx, x in enumerate(Images):
                Ext = x.rsplit('.', maxsplit=1)[-1]
                Hash = hashlib.md5(aEan.encode('utf-8')).hexdigest()[8::3]
                Dir = '/'.join(Hash[:2])
                Name = f'{Dir}/{Hash}_{aEan}_{Idx}.{Ext}'
                UrlD.append([x, Name, UrlSize.get(x, 0), aEan])

            DataImg = await self._ImgUpdate({
                    'method': 'UploadUrls',
                    'param': {
                        'aUrlD': UrlD,
                        'aDir': 'product/0',
                        'aDownload': True
                    }
                })
            assert('err' not in DataImg), DataImg['err']

            Res = []
            Status = DeepGetByList(DataImg, ['data', 'status'])
            if (Status):
                for xStatus, xUrlD in zip(Status, UrlD):
                    if (xStatus['status'] == 200):
                        Value = f"('{xUrlD[1]}', '{xStatus['url']}', {xStatus['size']}, now())"
                        Res.append(Value)
            return Res

        async def UpdateProduct(aEan: str, aInfo: dict, aImgValues: list):
            Features = json.dumps(aInfo['features'], ensure_ascii=False).replace("'", '`')
            Name = aInfo['name'].replace("'", '`')

            Query = f'''
                with
                    wrp as (
                        insert into ref_product0 (enabled)
                        values (true)
                        returning id
                    ),
                    wrpb as (
                        insert into ref_product0_barcode (product_id, code, product_en)
                        select
                            wrp.id,
                            '{aEan}',
                            'ean'
                        from wrp
                        on conflict (code, product_en) do nothing
                    ),
                    wrpl as (
                        insert into ref_product0_lang (product_id, lang_id, title, features)
                        select
                            wrp.id,
                            {self.Conf.LangId},
                            '{Name}',
                            '{Features}'
                        from wrp
                    ),
                    wrpi_1 as (
                        update ref_product0_image
                        set enabled = false
                        where product_id = (select wrp.id from wrp)
                    ),
                    wrpi_2 as (
                        insert into ref_product0_image (product_id, enabled, image, src_url, src_size, src_date)
                        select
                            wrp.id,
                            true,
                            t.image,
                            t.src_url,
                            t.src_size,
                            t.src_date
                        from wrp,
                        (values {', '.join(aImgValues)}) as t(image, src_url, src_size, src_date)
                        on conflict (product_id, image) do update
                        set enabled = true
                    ),
                    wrpc as (
                        insert into ref_product0_to_category (product_id, category_id)
                        select
                            wrp.id,
                            (select ref_product0_category_create({self.Conf.LangId}, '{aInfo.get('category')}'))
                        from wrp
                    )
                select id
                from wrp
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

        async def FetchSem(aEan: str, aSem: asyncio.Semaphore):
            async with aSem:
                Parser = await self.Parser(aEan)
                Info = DeepGetByList(Parser, ['data', 'product', 'pipe'])
                await UpdateCrawl(aEan, Parser['url'], Info)
                if (Info):
                    ImgValues = await UpdateImage(aEan, Info)
                    if (ImgValues):
                        await UpdateProduct(aEan, Info, ImgValues)
                else:
                    Log.Print(1, 'i', f"FetchSem(), ean {aEan} not found at {Parser['url']}")

        @DASplitDbl
        async def SProduct0(aDbl: TDbList, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct0()', aIdx, aLen)

            EanCrc = TEan()
            Values = []
            for Rec in aDbl:
                Ean = Rec.ean
                if (EanCrc.Init(Ean).Check()):
                    if (Ean.startswith('02')):
                        Log.Print(1, 'i', f'EAN internal {Ean}')
                    else:
                        Values.append(f"('{Ean}')")
                else:
                    Log.Print(1, 'i', f'EAN error {Ean}')

            Query = f'''
                select
                    t2.code
                from (
                    values {', '.join(Values)}
                ) as t2 (code)
                left join ref_product0_barcode rpb on
                    (t2.code = rpb.code) and (rpb.product_en = 'ean')
                left join ref_product0_crawl rpc on
                    (t2.code = rpc.code) and (rpc.product_en = 'ean')
                where
                    (rpc.code is null) or
                    ((rpb.code is null) and (rpc.info is null) and (DATE_PART('day', now() - rpc.update_date) > {self.Conf.MaxDays}))
            '''
            DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)

            if (not DblCur.IsEmpty()):
                Sem = asyncio.Semaphore(self.Conf.MaxConn)
                Tasks = [asyncio.create_task(FetchSem(Rec.code, Sem)) for Rec in DblCur]
                await asyncio.gather(*Tasks)

        self.ConfCrawl = await self.GetConfCrawl()
        Parsers = {'https://listex.info': self._Parse_ListexInfo}
        self.Parser = Parsers.get(self.Conf.SchemeUrl)
        assert(self.Parser), f'Unknown parser for {self.Conf.SchemeUrl}'

        await ReportCrawl()

        Log.Print(1, 'i', 'Product0')
        await SProduct0(aDbl, self.Conf.Parts)


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
            Parts = SqlDef.get('parts', 50),
            MaxConn = SqlDef.get('max_conn', 1)
        )

        ConfImg = self.Parent.Conf.GetKey('img_loader')
        ImgApi = TRequestJson(aAuth=TAuth(ConfImg.get('user'), ConfImg.get('password')))
        ImgApi.Url = ConfImg.get('url')

        self.Sql = TSql(aDb, SqlConf, ImgApi)


    async def InsertToDb(self, aDbCrawl: TDbCrawl):
        #await self.Sql.EanPotentialFind(aDbCrawl)
        #await self.Sql.EanRemoveBad()
        #await self.Sql.Product0_Create(aDbCrawl)
        pass
