# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from Inc.DbList  import TDbList, TDbRec
from Inc.DataClass import DDataClass
from Inc.Misc.Request import TRequestJson, TAuth
from Inc.ParserX.Common import TFileBase
from Inc.ParserX.CommonSql import TSqlBase, DASplit, TLogEx
from Inc.Sql.DbPg import TDbPg
from Inc.Sql.ADb import TDbExecPool, ListIntToComma
from Inc.Util.Obj import DeepGetByList
from IncP.Log import Log
from ..CommonDb import TDbCategory, TDbProductEx


@DDataClass
class TSqlConf():
    LangId: int
    TenantId: int
    PriceId: int
    AutoIdt: bool
    Parts: int = 100

class TCatalogToDb():
    def __init__(self, aDbl: TDbList):
        self.Dbl = aDbl
        self.BTree = self.Dbl.SearchAdd('id')

    def GetTree(self) -> dict:
        Res = {}
        for Rec in self.Dbl:
            ParentId = Rec.GetField('parent_id')
            Data = Res.get(ParentId, [])
            Data.append(Rec.id)
            Res[ParentId] = Data
        return Res

    def GetSequence(self, aTree: dict) -> list:
        def Recurs(aTree: dict, aParentId: int) -> list:
            ResR = []
            for x in aTree.get(aParentId, {}):
                RecNo = self.BTree.Search(x)
                Rec = self.Dbl.RecGo(RecNo)
                ResR.append({'id': x, 'parent_id': aParentId, 'name': Rec.name})
                if (x in aTree):
                    ResR += Recurs(aTree, x)
            return ResR
        return Recurs(aTree, 0)

    def Get(self) -> list:
        Tree = self.GetTree()
        Res = self.GetSequence(Tree)
        return Res


class TSql(TSqlBase):
    def __init__(self, aDb: TDbPg, aSqlConf: TSqlConf, aImgApi: TRequestJson):
        super().__init__()

        self.Db = aDb
        self.Conf = aSqlConf
        self.ImgApi = aImgApi
        self.CategoryIdt = {}
        self.ProductIdt = {}

    async def _ImgUpdate(self, aData):
        Url = f'{self.ImgApi.Url}/system'
        return await self.ImgApi.Send(Url, aData)

    async def DisableTable(self, aTable: str):
        Query = f'''
            update {aTable}
            set enabled = false
            where (tenant_id = {self.Conf.TenantId})
        '''
        await TDbExecPool(self.Db.Pool).Exec(Query)

    async def DisableTableByProduct(self, aTable: str, aCond: str = ''):
        Query = f'''
            update {aTable}
            set enabled = false
            where
                product_id in (
                    select id
                    from ref_product
                    where (tenant_id = {self.Conf.TenantId})
                )
                {aCond}
        '''
        await TDbExecPool(self.Db.Pool).Exec(Query)

    async def Category_Create(self, aData: list):
        async def Category(aData: list):
            Dbls: list[TDbList] = await SCategory(aData, self.Conf.Parts)
            Dbl = Dbls[0].New()
            Dbl.Append(Dbls)
            self.CategoryIdt = Dbl.ExportPair('idt', 'id')

        @DASplit
        async def SCategory(aData: list, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SCategory()', aIdx, aLen)

            Values = [f"({Row['id']}, {Row['parent_id']}, {self.Conf.TenantId})" for Row in aData]
            Query = f'''
                insert into ref_product_category (idt, parent_idt, tenant_id)
                values {', '.join(Values)}
                on conflict (idt, tenant_id) do update
                set enabled = true
                returning (id, idt)
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

            Ids = [Row['id'] for Row in aData]
            Query = f'''
                select id, idt
                from ref_product_category
                where idt in ({ListIntToComma(Ids)})
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplit
        async def SCategory_Lang(aData: list, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SCategory_Lang()', aIdx, aLen)

            Values = [
                f"({self.CategoryIdt[Row['id']]}, {self.Conf.LangId}, '{Row['name'].translate(self.Escape)}')"
                for Row in aData
            ]
            Query = f'''
                insert into ref_product_category_lang (category_id, lang_id, title)
                values {', '.join(Values)}
                on conflict (category_id, lang_id) do update
                set title = excluded.title
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

        Log.Print(1, 'i', 'Category')
        await self.DisableTable('ref_product_category')
        await Category(aData)

        Log.Print(1, 'i', 'Category_Lang')
        await SCategory_Lang(aData, self.Conf.Parts)

    async def Product_Create(self, aDbl: TDbProductEx):
        async def Product(aData: list):
            Dbls: list[TDbList] = await SProduct(aData, self.Conf.Parts)
            Dbl = Dbls[0].New()
            Dbl.Append(Dbls)
            self.ProductIdt = Dbl.ExportPair('idt', 'id')

        @DASplit
        async def SProduct(aData: list, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            nonlocal DbRec
            print('SProduct()', aIdx, aLen)

            if (self.Conf.AutoIdt):
                Values = [f"({self.Conf.TenantId}, '{DbRec.name.lower()}')" for DbRec.Data in aData]
                Values = ', '.join(Values)

                # (tenant_id, title) can be duplicated and DO UPDATE causes error. Use DO NOTHING
                Query = f'''
                    with
                        t1 as (
                            insert into ref_product_idt (tenant_id, title)
                            values {Values}
                            on conflict (tenant_id, title) do nothing
                            returning idt, title
                        ),
                        t2 as (
                            select idt,	title
                            from ref_product_idt
                            where (tenant_id, title) in ({Values})
                        )
                        select idt,	title
                        from t1
                        union all
                        table t2
                '''
                DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)

                Pairs = DblCur.ExportPair('title', 'idt')
                for DbRec.Data in aData:
                    Name = DbRec.name.lower()
                    Idt = Pairs.get(Name)
                    DbRec.SetField('id', Idt)

            Idts = []
            Values = []
            for DbRec.Data in aData:
                Idt = DbRec.GetField('id')

                Value = f'({Idt}, {self.Conf.TenantId}, {bool(DbRec.available)})'
                Values.append(Value)
                Idts.append(Idt)

            # (idt, tenant_id) can be duplicated and DO UPDATE causes error. Use DO NOTHING
            Query = f'''
                insert into ref_product (idt, tenant_id, enabled)
                values {', '.join(Values)}
                on conflict (idt, tenant_id)
                do nothing
                --do update
                --set enabled = excluded.enabled
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

            Query = f'''
                update ref_product
                set enabled = true
                where (tenant_id = {self.Conf.TenantId} and idt in ({ListIntToComma(Idts)}))
                returning id, idt
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplit
        async def SProduct_Lang(aData: list, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            nonlocal DbRec
            print('SProduct_Lang()', aIdx, aLen)

            Uniq = {}
            Values = []
            for DbRec.Data in aData:
                Key = (self.ProductIdt[DbRec.id], self.Conf.LangId)
                if (Key not in Uniq):
                    Uniq[Key] = ''

                    Descr = DbRec.GetField('descr', '').translate(self.Escape)
                    Feature = DbRec.GetField('feature', '')
                    Feature = json.dumps(Feature, ensure_ascii=False).replace("'", '`')
                    Value = f"({self.ProductIdt[DbRec.id]}, {self.Conf.LangId}, '{DbRec.name.translate(self.Escape)}', '{Descr}', '{Feature}')"
                    Values.append(Value)

            Query = f'''
                insert into ref_product_lang (product_id, lang_id, title, descr, feature)
                values {', '.join(Values)}
                on conflict (product_id, lang_id) do update
                set title = excluded.title, feature = excluded.feature, descr = excluded.descr
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplit
        async def SProduct_Image(aData: list, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            nonlocal DbRec
            print('SProduct_Image()', aIdx, aLen)

            Data = []
            ProductIds = []
            for DbRec.Data in aData:
                ProductId = self.ProductIdt[DbRec.id]
                ProductIds.append(ProductId)
                for xImage in DbRec.GetField('image', []):
                    Data.append({'product_id': ProductId, 'image': xImage.split('/')[-1], 'src_url': xImage})

            Query = f'''
                select id, product_id, image, src_url, src_size
                from ref_product_image
                where (product_id in ({ListIntToComma(ProductIds)}))
            '''
            DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)
            Urls = DblCur.ExportPair('src_url', 'src_size')

            UrlD = []
            for x in Data:
                Url = x['src_url']
                UrlD.append([Url, Urls.get(Url, 0), x['product_id']])

            DataImg = await self._ImgUpdate(
                {
                    'method': 'UploadUrls',
                    'param': {
                        'aUrlD': UrlD,
                        'aDir': f'product/{self.Conf.TenantId}',
                        'aDownload': True
                    }
                }
            )
            Status = DeepGetByList(DataImg, ['data', 'status'])
            if (Status):
                Values = []
                for Idx, x in enumerate(Status):
                    if (x['status'] == 200):
                        iData = Data[Idx]
                        Value = f"({iData['product_id']}, '{iData['image']}', '{iData['src_url']}', {x['size']}, now())"
                        Values.append(Value)

                Query = f'''
                    insert into ref_product_image (product_id, image, src_url, src_size, src_date)
                    values {', '.join(Values)}
                    on conflict (product_id, image) do update
                    set enabled = true, src_size = excluded.src_size, src_date = excluded.src_date
                    returning (id)
                '''
                await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplit
        async def SProduct_ToCategory(aData: list, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            nonlocal DbRec
            print('SProduct_ToCategory()', aIdx, aLen)

            Values = []
            for DbRec.Data in aData:
                Values.append(f'({self.ProductIdt[DbRec.id]}, {self.CategoryIdt[DbRec.category_id]})')

            Query = f'''
                insert into ref_product_to_category (product_id, category_id)
                values {', '.join(Values)}
                on conflict (product_id, category_id) do nothing
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplit
        async def SProduct_Price(aData: list, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            nonlocal DbRec
            print('SProduct_Price()', aIdx, aLen)

            Uniq = {}
            Values = []
            for DbRec.Data in aData:
                Key = (self.ProductIdt[DbRec.id], self.Conf.PriceId)
                if (Key not in Uniq):
                    Uniq[Key] = ''
                    Value = f'({self.ProductIdt[DbRec.id]}, {self.Conf.PriceId}, {DbRec.price})'
                    Values.append(Value)

            Query = f'''
                insert into ref_product_price (product_id, price_id, price)
                values {', '.join(Values)}
                on conflict (product_id, price_id, qty) do update
                set price = excluded.price
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)


        DbRec = TDbRec()
        DbRec.Fields = aDbl.Rec.Fields

        Log.Print(1, 'i', 'Product')
        await self.DisableTable('ref_product')
        await Product(aDbl.Data)

        Log.Print(1, 'i', 'Product_Lang')
        await SProduct_Lang(aDbl.Data, self.Conf.Parts)

        Log.Print(1, 'i', 'Product_ToCategory')
        await SProduct_ToCategory(aDbl.Data, self.Conf.Parts)

        Log.Print(1, 'i', 'Product_Price')
        await SProduct_Price(aDbl.Data, self.Conf.Parts)

        Log.Print(1, 'i', 'Product_Image')
        await self.DisableTableByProduct('ref_product_image', 'and (src_url is not null)')
        await SProduct_Image(aDbl.Data, self.Conf.Parts)


class TMain(TFileBase):
    def __init__(self, aParent, aDb: TDbPg, aExport: dict):
        super().__init__(aParent)

        ConfFile = self.Parent.GetFile()
        self.LogEx = TLogEx()
        self.LogEx = self.LogEx.Init(ConfFile)

        SqlDef = self.Parent.Conf.GetKey('sql', {})
        SqlDef.update(aExport.get('sql'))
        SqlConf = TSqlConf(
            TenantId = SqlDef.get('tenant_id'),
            LangId = SqlDef.get('lang_id'),
            PriceId = SqlDef.get('price_id'),
            Parts = SqlDef.get('parts', 50),
            AutoIdt = SqlDef.get('auto_idt', False)
        )

        ConfImg = self.Parent.Conf.GetKey('img_loader')
        ImgApi = TRequestJson(aAuth=TAuth(ConfImg.get('user'), ConfImg.get('password')))
        ImgApi.Url = ConfImg.get('url')

        self.Sql = TSql(aDb, SqlConf, ImgApi)


    async def InsertToDb(self, aDbCategory: TDbCategory, aDbProductEx: TDbProductEx):
        Data = TCatalogToDb(aDbCategory).Get()
        await self.Sql.Category_Create(Data)
        await self.Sql.Product_Create(aDbProductEx)
