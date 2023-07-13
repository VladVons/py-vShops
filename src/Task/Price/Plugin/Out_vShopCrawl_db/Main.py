# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import random
import json
import asyncio
import webbrowser
import lxml
from bs4 import BeautifulSoup
#
from Inc.DataClass import DDataClass
from Inc.DbList  import TDbList
from Inc.Ean import TEan
from Inc.Misc.Crypt import CryptSimple
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

def InputKey(aMsg: str, aKeys: list):
    while True:
        Answer = input(f"{aMsg} [{'/'.join(aKeys)}] :").lower()
        if (Answer in aKeys):
            return Answer

@DDataClass
class TSqlConf():
    lang_id: int
    parser: str
    max_days: int = 30
    parts: int = 100
    max_conn: int = 1
    rand_sleep: list = [0.25, 1.0]

class TSql(TSqlBase):
    def __init__(self, aDb: TDbPg, aSqlConf: TSqlConf, aImgApi: TRequestJson):
        super().__init__(aDb)

        self.Conf = aSqlConf
        self.ImgApi = aImgApi
        self.ConfCrawl: TDbList
        self.Parser: TParserBase = None
        self.TenantId = 0

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

    async def CodeNullInfo(self):
        Query = f'''
            select code
            from ref_product0_crawl rpc
            where (product_en = '{self.Parser.CodeType}') and (info is null)
        '''
        return await TDbExecPool(self.Db.Pool).Exec(Query)

    async def EanPotentialFind(self, aDbl: TDbList):
        Dbl = await self.CodeNullInfo()
        Pairs = Dbl.ExportPair('code', 1)
        Res = [Rec.code for Rec in aDbl if Rec.code in Pairs]
        print(f'Need ean: {len(Dbl)}, records in file: {len(aDbl)}, matches: {len(Res)}')

    async def EanRemoveBad(self):
        assert(self.Parser.CodeType == 'ean'), 'Not ean parser'

        EanCrc = TEan()
        Eans = []
        DblCur = await self.CodeNullInfo()
        for Rec in DblCur:
            Code = Rec.code.strip()
            if (len(Code) < 8) or (Code.startswith('02')) or (not EanCrc.Init(Code).Check()):
                Eans.append(Code)

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

        async def UpdateCrawl(aCode: str, aInfo: dict):
            if (aInfo):
                Url = "'" + aInfo.get('url', '') + "'"
                Info = "'" + json.dumps(aInfo, ensure_ascii=False).replace("'", '`') + "'"
            else:
                Url = 'null'
                Info = 'null'

            Query = f'''
                insert into ref_product0_crawl (code, product_en, url, update_date, info, crawl_site_id)
                values ('{aCode}', '{self.Parser.CodeType}', {Url}, now(), {Info}, {self.ConfCrawl.Rec.id})
                on conflict (code, product_en, crawl_site_id) do update
                set update_date = now(), info = {Info}
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

        async def UpdateImage(aCode: str, aInfo: dict) -> list:
            Images = aInfo.get('images', [])
            if (isinstance(Images, str)):
                Images = [Images]

            if (not Images):
                return

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
                #Hash = hashlib.md5(aCode.encode('utf-8')).hexdigest()[8::3]
                #Dir = '/'.join(Hash[:2])
                #Name = f'{Dir}/{Hash}_{aCode}_{Idx}.{Ext}'
                CodeX = CryptSimple(aCode, 71)
                Name = f'{self.TenantId}/{self.Parser.CodeType[::-1]}/{CodeX[-2:]}/{CodeX}_{Idx}.{Ext}'

                if (self.Parser.Moderate):
                    webbrowser.open(x, new=0, autoraise=False)
                    print()
                    print(f"Code: {aCode}, name {aInfo['name']}, {Idx}")
                    print('\n'.join(Images[Idx:]))
                    Answer = InputKey('Add image ?', ['y', 'n', 'c'])
                    if (Answer == 'y'):
                        UrlD.append([x, Name, UrlSize.get(x, 0), aCode])
                    elif (Answer == 'c'):
                        break
                else:
                    UrlD.append([x, Name, UrlSize.get(x, 0), aCode])

            if (not UrlD):
                return []

            DataImg = await self._ImgUpdate({
                    'method': 'UploadUrls',
                    'param': {
                        'aUrlD': UrlD,
                        'aDir': 'product',
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

        async def UpdateProduct(aCode: str, aInfo: dict, aImgValues: list):
            Name = aInfo.get('name', '').replace("'", '`')
            Descr = GetNotNone(aInfo, 'descr', '').replace("'", '`')
            Category = GetNotNone(aInfo, 'category', '_???').replace("'", '`')

            Features = aInfo.get('features')
            if (Features):
                Features = "'" + json.dumps(aInfo.get('features', {}), ensure_ascii=False).replace("'", '`') + "'"
            else:
                Features = 'null'

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
                            '{aCode}',
                            '{self.Parser.CodeType}'
                        from wrp
                        on conflict (code, product_en) do nothing
                    ),
                    wrpl as (
                        insert into ref_product0_lang (product_id, lang_id, title, features, descr)
                        select
                            wrp.id,
                            {self.Conf.lang_id},
                            '{Name}',
                            {Features},
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
                            (select ref_product0_category_create({self.Conf.lang_id}, '{Category}'))
                        from wrp
                    )
                select id
                from wrp
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

        async def FetchSem(aCode: str, aSem: asyncio.Semaphore):
            # debug
            async with aSem:
                if (self.Conf.rand_sleep):
                    Sleep = random.uniform(*self.Conf.rand_sleep)
                    await asyncio.sleep(Sleep)

                Info = await self.Parser.GetData(aCode)
                await UpdateCrawl(aCode, Info)
                if (Info):
                    ImgValues = await UpdateImage(aCode, Info)
                    if (ImgValues):
                        await UpdateProduct(aCode, Info, ImgValues)
                else:
                    Log.Print(1, 'i', f"FetchSem(), code {aCode} not found at {self.Parser.UrlRoot}")

        @DASplitDbl
        async def SProduct0(aDbl: TDbList, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct0()', aIdx, aLen)

            Values = []
            for Rec in aDbl:
                Values.append(f"('{Rec.code}')")

            Query = f'''
                with
                    wt1	as (
                        select
                            t2.code
                        from (
                            values {', '.join(Values)}
                        ) as t2 (code)
                        left join ref_product0_barcode rpb on
                            (t2.code = rpb.code) and (rpb.product_en = '{self.Parser.CodeType}')
                        where
                            (rpb.code is null)
                )
                select wt1.code
                from wt1
                left join ref_product0_crawl rpc on
                    (wt1.code = rpc.code) and (rpc.product_en = '{self.Parser.CodeType}') and (rpc.crawl_site_id = {self.ConfCrawl.Rec.id})
                where
                    (
                        (rpc.info is null) and
                        (DATE_PART('day', now() - rpc.update_date) > {self.Conf.max_days}) and
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
                Sem = asyncio.Semaphore(self.Conf.max_conn)
                Tasks = [asyncio.create_task(FetchSem(Rec.code, Sem)) for Rec in DblCur]
                await asyncio.gather(*Tasks)

        PluginEan = TPluginEan('IncP/PluginEan')
        self.Parser = PluginEan.Load(self.Conf.parser)
        await self.Parser.Init()
        self.ConfCrawl = await self.GetConfCrawl(self.Parser.UrlRoot)
        assert(not self.ConfCrawl.IsEmpty()), f'No DB config for {self.Parser.UrlRoot}'

        await ReportCrawl()

        Log.Print(1, 'i', 'Product0')
        await SProduct0(aDbl, self.Conf.parts)


class TMain(TFileBase):
    def __init__(self, aParent, aDb: TDbPg):
        super().__init__(aParent)

        ConfFile = self.Parent.GetFile()
        self.LogEx = TLogEx()
        self.LogEx = self.LogEx.Init(ConfFile)

        SqlDef = self.Parent.Conf.GetKey('sql', {})
        SqlConf = TSqlConf(**SqlDef)

        ConfImg = self.Parent.Conf.GetKey('img_loader')
        ImgApi = TRequestJson(aAuth=TAuth(ConfImg.get('user'), ConfImg.get('password')))
        ImgApi.Url = ConfImg.get('url')

        self.Sql = TSql(aDb, SqlConf, ImgApi)


    async def InsertToDb(self, aDbCrawl: TDbCrawl):
        #await self.Sql.EanPotentialFind(aDbCrawl)
        #await self.Sql.EanRemoveBad()
        await self.Sql.Product0_Create(aDbCrawl)
