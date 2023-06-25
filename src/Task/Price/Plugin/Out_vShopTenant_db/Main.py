# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from Inc.DataClass import DDataClass
from Inc.DbList import TDbList
from Inc.Misc.Request import TRequestJson, TAuth
from Inc.ParserX.Common import TFileBase
from Inc.ParserX.CommonSql import TSqlBase, DASplit, DASplitDbl, TLogEx
from Inc.Sql.ADb import TDbExecPool, ListIntToComma, ListToComma
from Inc.Sql.DbPg import TDbPg
from Inc.Util.Obj import DeepGetByList
from Inc.Util.Str import ToHashW
from IncP.Log import Log
from ..CommonDb import TDbCategory, TDbProductEx


@DDataClass
class TSqlConf():
    lang_id: int
    tenant_id: int
    price_id: int
    auto_idt: bool = False
    parts: int = 100

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
            where (tenant_id = {self.Conf.tenant_id})
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
                    where (tenant_id = {self.Conf.tenant_id})
                )
                {aCond}
        '''
        await TDbExecPool(self.Db.Pool).Exec(Query)

    async def ProductModelUnknown(self):
        Query = f'''
            select
		        rp.model,
		        count(*)
            from
                ref_product rp
            left join
                ref_product_product0 rpp on
                (rpp.tenant_id = {self.Conf.tenant_id}) and (rpp.product_en = 'model') and (rpp.code = rp.model)
            where
                (rp.enabled) and (rp.model is not null) and (rp.tenant_id = {self.Conf.tenant_id}) and (rpp.code is null)
            group by
                model
            order by
                model
        '''
        return await TDbExecPool(self.Db.Pool).Exec(Query)

    async def Category_Create(self, aData: list):
        async def Category(aData: list):
            Dbls: list[TDbList] = await SCategory(aData, self.Conf.parts)
            Dbl = Dbls[0].New()
            Dbl.Append(Dbls)
            self.CategoryIdt = Dbl.ExportPair('idt', 'id')

        @DASplit
        async def SCategory(aData: list, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SCategory()', aIdx, aLen)

            Values = [f"({Row['id']}, {Row['parent_id']}, {self.Conf.tenant_id})" for Row in aData]
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
                f"({self.CategoryIdt[Row['id']]}, {self.Conf.lang_id}, '{Row['name'].translate(self.Escape)}')"
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
        await SCategory_Lang(aData, self.Conf.parts)

    async def Product_Create(self, aDbl: TDbProductEx):
        async def Product(aData: list):
            Dbls: list[TDbList] = await SProduct(aData, self.Conf.parts)
            Dbl = Dbls[0].New()
            Dbl.Append(Dbls)
            self.ProductIdt = Dbl.ExportPair('idt', 'id')

        @DASplitDbl
        async def SProduct(aDbl: TDbProductEx, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct()', aIdx, aLen)

            if (self.Conf.auto_idt):
                Values = [f"({self.Conf.tenant_id}, '{ToHashW(Rec.name)}')" for Rec in aDbl]
                Values = ', '.join(Values)

                # (tenant_id, title) can be duplicated and DO UPDATE causes error. Use DO NOTHING
                Query = f'''
                    with
                        t1 as (
                            insert into ref_product_idt (tenant_id, hash)
                            values {Values}
                            on conflict (tenant_id, hash) do nothing
                            returning idt, hash
                        ),
                        t2 as (
                            select idt,	hash
                            from ref_product_idt
                            where (tenant_id, hash) in ({Values})
                        )
                        select idt, hash
                        from t1
                        union all
                        table t2
                '''
                DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)

                Pairs = DblCur.ExportPair('hash', 'idt')
                for Rec in aDbl:
                    Idt = Pairs.get(ToHashW(Rec.name))
                    Rec.SetField('id', Idt)

            Uniq = {}
            Values = []
            for Rec in aDbl:
                Idt = Rec.GetField('id')
                Key = (Idt, self.Conf.tenant_id)
                if (Key not in Uniq):
                    Uniq[Key] = ''

                    Value = f"({Idt}, {self.Conf.tenant_id}, {bool(Rec.available)}, '{Rec.model}')"
                    Values.append(Value)

            if (Values):
                Query = f'''
                    insert into ref_product (idt, tenant_id, enabled, model)
                    values {', '.join(Values)}
                    on conflict (idt, tenant_id) do update
                    set enabled = excluded.enabled, model = excluded.model
                    returning id, idt
                '''
                return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplitDbl
        async def SProduct_Product0(aDbl: TDbProductEx, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct_Product()', aIdx, aLen)

            Models = aDbl.ExportList('model')
            Query = f'''
                with wrp as (
                    select
                        rp.id as protuct_id,
                        rpp.product0_id
                    from
                        ref_product rp
                    left join
                        ref_product_product0 rpp on
                        (rpp.tenant_id = {self.Conf.tenant_id}) and (rpp.product_en = 'model') and (rpp.code = rp.model)
                    where
                        (rp.enabled) and
                        (rp.model is not null) and
                        (rp.tenant_id = {self.Conf.tenant_id}) and
                        (rp.model in ({ListToComma(Models)})) and
                        (rpp.enabled) and
                        (rpp.code is not null)
                )
                update
                    ref_product rp
                set
                    product0_id = subquery.product_id
                from (
                    select
                        protuct_id,
                        product0_id
                    from
                        wrp
                ) as subquery (id, product_id)
                where
                    (rp.id = subquery.id)
                returning
                    rp.id, rp.product0_id
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplitDbl
        async def SProduct_Lang(aDbl: TDbProductEx, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct_Lang()', aIdx, aLen)

            Uniq = {}
            Values = []
            for Rec in aDbl:
                Key = (self.ProductIdt[Rec.id], self.Conf.lang_id)
                if (Key not in Uniq):
                    Uniq[Key] = ''

                    Descr = Rec.GetField('descr', '').translate(self.Escape)
                    Features = Rec.GetField('features', '')
                    Features = json.dumps(Features, ensure_ascii=False).replace("'", '`')
                    Value = f"({self.ProductIdt[Rec.id]}, {self.Conf.lang_id}, '{Rec.name.translate(self.Escape)}', '{Descr}', '{Features}')"
                    Values.append(Value)

            Query = f'''
                insert into ref_product_lang (product_id, lang_id, title, descr, features)
                values {', '.join(Values)}
                on conflict (product_id, lang_id) do update
                set title = excluded.title, features = excluded.features, descr = excluded.descr
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplitDbl
        async def SProduct_Image(aDbl: TDbProductEx, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct_Image()', aIdx, aLen)

            Data = []
            ProductIds = []
            for Rec in aDbl:
                ProductId = self.ProductIdt[Rec.id]
                ProductIds.append(ProductId)
                for xImage in Rec.GetField('image', []):
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
                UrlD.append([Url, None, Urls.get(Url, 0), x['product_id']])

            DataImg = await self._ImgUpdate(
                {
                    'method': 'UploadUrls',
                    'param': {
                        'aUrlD': UrlD,
                        'aDir': f'product/{self.Conf.tenant_id}',
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

        @DASplitDbl
        async def SProduct_ToCategory(aDbl: TDbProductEx, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct_ToCategory()', aIdx, aLen)

            Values = []
            for Rec in aDbl:
                Values.append(f'({self.ProductIdt[Rec.id]}, {self.CategoryIdt[Rec.category_id]})')

            Query = f'''
                insert into ref_product_to_category (product_id, category_id)
                values {', '.join(Values)}
                on conflict (product_id, category_id) do nothing
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplitDbl
        async def SProduct_Price(aDbl: TDbProductEx, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct_Price()', aIdx, aLen)

            Uniq = {}
            Values = []
            for Rec in aDbl:
                Key = (self.ProductIdt[Rec.id], self.Conf.price_id)
                if (Key not in Uniq):
                    Uniq[Key] = ''
                    Value = f'({self.ProductIdt[Rec.id]}, {self.Conf.price_id}, {Rec.price})'
                    Values.append(Value)

            Query = f'''
                insert into ref_product_price (product_id, price_id, price)
                values {', '.join(Values)}
                on conflict (product_id, price_id, qty) do update
                set price = excluded.price
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)


        Log.Print(1, 'i', 'Product')
        await self.DisableTable('ref_product')
        await Product(aDbl)

        Log.Print(1, 'i', 'Product_Lang')
        await SProduct_Lang(aDbl, self.Conf.parts)

        Log.Print(1, 'i', 'Product_ToCategory')
        await SProduct_ToCategory(aDbl, self.Conf.parts)

        Log.Print(1, 'i', 'Product_Price')
        await SProduct_Price(aDbl, self.Conf.parts)

        Log.Print(1, 'i', 'Product_Image')
        await self.DisableTableByProduct('ref_product_image', 'and (src_url is not null)')
        await SProduct_Image(aDbl, self.Conf.parts)

        Log.Print(1, 'i', 'Product_Product0')
        await SProduct_Product0(aDbl, self.Conf.parts)

class TMain(TFileBase):
    def __init__(self, aParent, aDb: TDbPg, aExport: dict):
        super().__init__(aParent)

        ConfFile = self.Parent.GetFile()
        self.LogEx = TLogEx()
        self.LogEx = self.LogEx.Init(ConfFile)

        SqlDef = self.Parent.Conf.GetKey('sql', {})
        SqlDef.update(aExport.get('sql'))
        SqlConf = TSqlConf(**SqlDef)

        ConfImg = self.Parent.Conf.GetKey('img_loader')
        ImgApi = TRequestJson(aAuth=TAuth(ConfImg.get('user'), ConfImg.get('password')))
        ImgApi.Url = ConfImg.get('url')

        self.Sql = TSql(aDb, SqlConf, ImgApi)


    async def InsertToDb(self, aDbCategory: TDbCategory, aDbProductEx: TDbProductEx):
        Data = TCatalogToDb(aDbCategory).Get()
        await self.Sql.Category_Create(Data)
        await self.Sql.Product_Create(aDbProductEx)
