# Created: 2024.06.10
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
    lang: str
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
            DblCodes = await TDbExecPool(self.Db.Pool).Exec(Query)
            CodePairs = DblCodes.ExportPair('code', 'product_id')

            Models = aDbl.ExportList('model')
            Query = f'''
                select
                    rp.model,
                    rp.tenant_id
                from
                    ref_product rp
                where
                    (model in ({ListToComma(Models)}))
            '''
            DblModels = await TDbExecPool(self.Db.Pool).Exec(Query)

            ModelPairs = {}
            for Rec in DblModels:
                Model = Rec.model
                if (Model not in ModelPairs):
                    ModelPairs[Model] = []

                if (Rec.tenant_id not in ModelPairs[Model]):
                    ModelPairs[Model].append(Rec.tenant_id)

            Values = []
            for Rec in aDbl:
                ProductId = CodePairs.get(Rec.code)
                if (ProductId):
                    TenantIds = ModelPairs.get(Rec.model, [])
                    for xTenantId in TenantIds:
                        Values.append(f"('{Rec.model}', 'model', {ProductId}, {xTenantId})")

            if (Values):
                # no serial column
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
        await self.Sql.Product0(aDbCrawl)
