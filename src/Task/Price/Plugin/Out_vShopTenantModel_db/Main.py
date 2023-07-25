# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DataClass import DDataClass
from Inc.DbList  import TDbList
from Inc.ParserX.Common import TFileBase
from Inc.ParserX.CommonSql import TSqlBase, TLogEx, DASplitDbl
from Inc.Sql import TDbExecPool, TDbPg, ListToComma
from IncP.Log import Log
from ..CommonDb import TDbCrawl


@DDataClass
class TSqlConf():
    lang_id: int
    alias: str
    parts: int = 100

class TSql(TSqlBase):
    def __init__(self, aDb: TDbPg, aSqlConf: TSqlConf):
        super().__init__(aDb)

        self.Conf = aSqlConf

    async def Product0(self, aDbl: TDbCrawl):
        @DASplitDbl
        async def SProduct0(aDbl: TDbList, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct0()', aIdx, aLen)

            Codes = aDbl.ExportList('code')
            Query = f'''
                select
                    rpb.code,
                    rpb.product_id
                from
                    ref_product0_barcode rpb
                where
                    (product_en = 'icecat') and
                    (code in ({ListToComma(Codes)}))
            '''
            DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)
            Pairs = DblCur.ExportPair('code', 'product_id')

            Values = []
            for Rec in aDbl:
                ProductId = Pairs.get(Rec.code)
                if (ProductId):
                    Values.append(f"('{Rec.model}', 'model', {ProductId}, {self.tenant_id})")

            if (Values):
                Query = f'''
                    insert into ref_product_product0(code, product_en, product0_id, tenant_id)
                    values {', '.join(Values)}
                    on conflict (tenant_id, code, product_en) do nothing
                '''
                await TDbExecPool(self.Db.Pool).Exec(Query)

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
        self.Sql = TSql(aDb, SqlConf)

    async def InsertToDb(self, aDbCrawl: TDbCrawl):
        await self.Sql.LoadTenantConf(self.Sql.Conf.alias)
        await self.Sql.Product0(aDbCrawl)
