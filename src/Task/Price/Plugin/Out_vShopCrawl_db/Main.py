# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
# 4823096802060 long name
# '3086126726984'


import re
import random
import json
import asyncio
import hashlib
import webbrowser
import lxml
from bs4 import BeautifulSoup
#
from Inc.DataClass import DDataClass
from Inc.DbList  import TDbList
from Inc.Ean import TEan
from Inc.Misc.Request import TRequestJson, TAuth
from Inc.ParserX.Common import TFileBase
from Inc.ParserX.CommonSql import TSqlBase, DASplitDbl, TLogEx
from Inc.Sql import TDbExecPool, TDbPg, ListToComma
from Inc.Util.Obj import DeepGetByList, GetNotNone
from IncP.Log import Log
from IncP.PluginEan import TPluginEan, TParserBase
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
    Parser: str
    MaxDays: int = 30
    Parts: int = 100
    MaxConn: int = 1
    RandSleep: list = []

class TSql(TSqlBase):
    def __init__(self, aDb: TDbPg, aSqlConf: TSqlConf, aImgApi: TRequestJson):
        super().__init__()

        self.Db = aDb
        self.Conf = aSqlConf
        self.ImgApi = aImgApi
        self.ConfCrawl: TDbList
        self.Parser: TParserBase = None

    async def GetConfCrawl(self, aHost: str) -> TDbList:
        Query = f'''
            select
                id, scheme, max_days
            from
                ref_crawl_site rcs
            where
                (enabled) and (url = '{aHost}')
        '''
        return await TDbExecPool(self.Db.Pool).Exec(Query)

    async def _ImgUpdate(self, aData):
        Url = f'{self.ImgApi.Url}/system'
        return await self.ImgApi.Send(Url, aData)

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
            # Query = '''
            #     select
            #         count(*) as ean_all,
            #         count(info) as ean_yes,
            #         count(case when info is null then 1 end) as ean_no
            #     from
            #         ref_product0_crawl rpc
            # '''
            Query = '''
                select
                    (select count(distinct code) from ref_product0_crawl) as ean_all,
                    (select count(distinct code) from ref_product0_crawl where (info is not null)) as ean_yes,
                    (select count(distinct code) from ref_product0_crawl where (info is null)) as ean_no
            '''

            DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)
            Log.Print(1, 'i', f'ReportCrawl(), {DblCur.Rec.GetAsDict()}')

        async def UpdateCrawl(aEan: str, aInfo: dict):
            if (aInfo):
                Url = "'" + aInfo.get('url', '') + "'"
                Info = "'" + json.dumps(aInfo, ensure_ascii=False).replace("'", '`') + "'"
            else:
                Url = 'null'
                Info = 'null'

            Query = f'''
                insert into ref_product0_crawl (code, product_en, url, update_date, info, crawl_site_id)
                values ('{aEan}', 'ean', {Url}, now(), {Info}, {self.ConfCrawl.Rec.id})
                on conflict (code, product_en, crawl_site_id) do update
                set update_date = now(), info = {Info}
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

        async def UpdateImage(aEan: str, aInfo: dict) -> list:
            Images = aInfo.get('images', [])
            if (isinstance(Images, str)):
                Images = [Images]

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

                if (self.Parser.Moderate):
                    webbrowser.open(x, new=0, autoraise=False)
                    print()
                    print(f"ean: {aEan}, name {aInfo['name']}")
                    print(f'image: {x}')
                    Answer = input('add image y/n ?:')
                    if (Answer != 'y'):
                        continue

                UrlD.append([x, Name, UrlSize.get(x, 0), aEan])

            if (not UrlD):
                return []

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
            Name = aInfo.get('name', '').replace("'", '`')
            Descr = GetNotNone(aInfo, 'descr', '').replace("'", '`')
            Category = GetNotNone(aInfo, 'category', '_???').replace("'", '`')
            Features = json.dumps(aInfo.get('features', {}), ensure_ascii=False).replace("'", '`')

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
                        insert into ref_product0_lang (product_id, lang_id, title, features, descr)
                        select
                            wrp.id,
                            {self.Conf.LangId},
                            '{Name}',
                            '{Features}',
                            '{Descr}'
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
                            (select ref_product0_category_create({self.Conf.LangId}, '{Category}'))
                        from wrp
                    )
                select id
                from wrp
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

        async def FetchSem(aEan: str, aSem: asyncio.Semaphore):
            # core
            async with aSem:
                if (self.Conf.RandSleep):
                    Sleep = random.uniform(*self.Conf.RandSleep)
                    await asyncio.sleep(Sleep)

                Info = await self.Parser.GetData(aEan)
                await UpdateCrawl(aEan, Info)
                if (Info):
                    ImgValues = await UpdateImage(aEan, Info)
                    if (ImgValues):
                        await UpdateProduct(aEan, Info, ImgValues)
                else:
                    Log.Print(1, 'i', f"FetchSem(), ean {aEan} not found at {self.Parser.UrlRoot}")

        @DASplitDbl
        async def SProduct0(aDbl: TDbList, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct0()', aIdx, aLen)

            Values = []
            for Rec in aDbl:
                Ean = Rec.ean
                if (Ean.startswith('02')):
                    Log.Print(1, 'i', f'EAN internal {Ean}')
                elif (not re.match(self.Parser.EanAllow, Ean)):
                    Log.Print(1, 'i', f'EAN filter {Ean}')
                elif (not TEan(Ean).Check()):
                    Log.Print(1, 'i', f'EAN error {Ean}')
                else:
                    Values.append(f"('{Ean}')")

            Query = f'''
                with
                    wt1	as (
                        select
                            t2.code
                        from (
                            values {', '.join(Values)}
                        ) as t2 (code)
                        left join ref_product0_barcode rpb on
                            (t2.code = rpb.code) and (rpb.product_en = 'ean')
                        where
                            (rpb.code is null)
                )
                select wt1.code
                from wt1
                left join ref_product0_crawl rpc on
                    (wt1.code = rpc.code) and (rpc.product_en = 'ean') and (rpc.crawl_site_id = {self.ConfCrawl.Rec.id})
                where
                    (
                        (rpc.info is null) and
                        (DATE_PART('day', now() - rpc.update_date) > {self.Conf.MaxDays}) and
                        (rpc.url like '{self.Parser.UrlRoot}%')
                    )
                    or
                    (
                        (rpc.code is null)
                    )
            '''
            #print(Query)
            DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)

            if (not DblCur.IsEmpty()):
                Sem = asyncio.Semaphore(self.Conf.MaxConn)
                Tasks = [asyncio.create_task(FetchSem(Rec.code, Sem)) for Rec in DblCur]
                await asyncio.gather(*Tasks)

        PluginEan = TPluginEan('IncP/PluginEan')
        self.Parser = PluginEan.Load(self.Conf.Parser)
        await self.Parser.Init()
        self.ConfCrawl = await self.GetConfCrawl(self.Parser.UrlRoot)
        assert(not self.ConfCrawl.IsEmpty()), f'No DB config for {self.Parser.UrlRoot}'

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
            Parser = SqlDef.get('parser'),
            Parts = SqlDef.get('parts', 50),
            MaxConn = SqlDef.get('max_conn', 1),
            RandSleep = SqlDef.get('rand_sleep', []),
        )

        ConfImg = self.Parent.Conf.GetKey('img_loader')
        ImgApi = TRequestJson(aAuth=TAuth(ConfImg.get('user'), ConfImg.get('password')))
        ImgApi.Url = ConfImg.get('url')

        self.Sql = TSql(aDb, SqlConf, ImgApi)


    async def InsertToDb(self, aDbCrawl: TDbCrawl):
        #await self.Sql.EanPotentialFind(aDbCrawl)
        #await self.Sql.EanRemoveBad()
        await self.Sql.Product0_Create(aDbCrawl)
