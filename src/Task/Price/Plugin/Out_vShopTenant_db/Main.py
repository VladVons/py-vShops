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
from Inc.Util.Num import RoundNear
from IncP.Log import Log
from ..CommonDb import TDbCategory, TDbProductEx


@DDataClass
class TSqlConf():
    lang: str
    tenant: str
    product0: str
    currency: str = ''
    idt_auto: bool = False
    parts: int = 100
    min_qty: int = 0
    price_round: int = 1
    price_auto: bool = False

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
        def Recurs(aParentId: int) -> list:
            ResR = []
            for x in aTree.get(aParentId, {}):
                RecNo = self.BTree.Search(x)
                Rec = self.Dbl.RecGo(RecNo)
                ResR.append({'id': x, 'parent_id': aParentId, 'name': Rec.name})
                if (x in aTree):
                    ResR += Recurs(x)
            return ResR
        return Recurs(0)

    def Get(self) -> list:
        Tree = self.GetTree()
        Res = self.GetSequence(Tree)
        return Res


class TSql(TSqlBase):
    def __init__(self, aDb: TDbPg, aSqlConf: TSqlConf, aImgApi: TRequestJson):
        super().__init__(aDb)

        self.Conf = aSqlConf
        self.ImgApi = aImgApi
        self.CategoryIdt = {}
        self.ProductIdt = {}
        self.CurrencyRate = 1

    async def _ImgUpdate(self, aData):
        Url = f'{self.ImgApi.Url}/system'
        return await self.ImgApi.Send(Url, aData)

    async def DisableTable(self, aTable: str):
        Query = f'''
            update {aTable}
            set enabled = false
            where (tenant_id = {self.tenant_id})
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
                    where (tenant_id = {self.tenant_id})
                )
                {aCond}
        '''
        await TDbExecPool(self.Db.Pool).Exec(Query)

    async def ProductModelUnknown(self):
        return await self.ExecQuery(__package__, 'fmtGet_ModelUnknown.sql', {'aTenantId': self.tenant_id})

    async def GetProductsMargin(self, aProductIds: list[int]):
        Res = {}
        ProductIds = ListIntToComma(aProductIds)
        Dbl = await self.ExecQuery(__package__, 'fmtGet_ProductMargin.sql', {'aProductIds': ProductIds})
        for Rec in Dbl:
            PrevMargin = 1
            for xMargin in Rec.margin:
                PrevMargin = xMargin if xMargin else PrevMargin
            Res[Rec.product_id] = PrevMargin
        return Res

    async def GetCurrencyRate(self):
        if (self.Conf.currency):
            Query = f'''
                select alias, rate::float
                from ref_currency
                where enabled and alias = '{self.Conf.currency}'
            '''
            Dbl = await TDbExecPool(self.Db.Pool).Exec(Query)
            assert (not Dbl.IsEmpty()), f'Unknown currency {self.Conf.currency}'
            self.CurrencyRate = Dbl.Rec.rate

    async def Category_Create(self, aData: list):
        async def Category(aData: list):
            # Query = f'''
            #     insert into ref_product_category (idt, tenant_id)
            #     values (0, {self.tenant_id})
            #     on conflict (idt, tenant_id) do nothing
            # '''
            Query = f'''
                insert into ref_product_category (idt, tenant_id)
                select idt, tenant_id
                from (values (0, {self.tenant_id})) src(idt, tenant_id)
                where not exists (
                    select 1 from ref_product_category dst where (dst.idt = src.idt) and (dst.tenant_id = src.tenant_id)
                )
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

            Dbls: list[TDbList] = await SCategory(aData, self.Conf.parts)
            Dbl = Dbls[0].New()
            Dbl.Append(Dbls)
            self.CategoryIdt = Dbl.ExportPair('idt', 'id')

        @DASplit
        async def SCategory(aData: list, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SCategory()', aIdx, aLen)

            Values = [f"({Row['id']}, {Row['parent_id']}, {self.tenant_id})" for Row in aData]
            # Query = f'''
            #     insert into ref_product_category (idt, parent_idt, tenant_id)
            #     values {', '.join(Values)}
            #     on conflict (idt, tenant_id) do update
            #     set enabled = true
            #     returning (id, idt)
            # '''
            Query = f'''
                with src (idt, parent_idt, tenant_id) as (
                    values {', '.join(Values)}
                )
                merge into ref_product_category as dst
                using src
                on (dst.idt = src.idt) and (dst.tenant_id = src.tenant_id)
                when matched then
                    update set enabled = true
                when not matched then
                    insert (idt, parent_idt, tenant_id)
                    values (src.idt, src.parent_idt, src.tenant_id)
                '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

            Ids = [Row['id'] for Row in aData]
            Query = f'''
                select id, idt
                from ref_product_category
                where (tenant_id = {self.tenant_id}) and (idt in ({ListIntToComma(Ids)}))
            '''
            Res = await TDbExecPool(self.Db.Pool).Exec(Query)
            return Res

        @DASplit
        async def SCategory_Lang(aData: list, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SCategory_Lang()', aIdx, aLen)

            Values = [
                f"({self.CategoryIdt[Row['id']]}, {self.lang_id}, '{Row['name'].translate(self.Escape)}')"
                for Row in aData
            ]
            # no serial column
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
        def GetUnique(aDbl: TDbProductEx) -> TDbList:
            Uniq = {}
            Res = aDbl.New()
            for Rec in aDbl:
                Id = Rec.id
                if (Id in Uniq):
                    print()
                    Log.Print(1, 'i', f'Not uniq ID. {Rec.GetAsDictVal()}')
                    Log.Print(1, 'i', f'Prev record. {Uniq.get(Id)}')
                else:
                    if (Rec.qty >= self.Conf.min_qty):
                        Uniq[Id] = Rec.GetAsDictVal()
                        Res.RecAdd(Rec.Data)
            return Res

        async def Product(aDbl: TDbProductEx):
            Dbls: list[TDbList] = await SProduct(aDbl, self.Conf.parts)
            Dbl = Dbls[0].New()
            Dbl.Append(Dbls)
            self.ProductIdt = Dbl.ExportPair('idt', 'id')

        @DASplitDbl
        async def SProduct(aDbl: TDbProductEx, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            async def SetAutoIdt():
                Values = [f"({self.tenant_id}, '{ToHashW(Rec.name)}')" for Rec in aDbl]
                Values = ', '.join(Values)

                # (tenant_id, title) can be duplicated and DO UPDATE causes error. Use DO NOTHING
                # on insert ref_product_idt causes insert into ref_product too
                # no serial column
                Query = f'''
                    with
                        wt1 as (
                            insert into ref_product_idt (tenant_id, hash)
                            values {Values}
                            on conflict (tenant_id, hash) do nothing
                            returning idt, hash
                        ),
                        wt2 as (
                            select idt,	hash
                            from ref_product_idt
                            where (tenant_id, hash) in ({Values})
                        )
                        select idt, hash
                        from wt1
                        union all
                        table wt2
                '''
                DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)

                Pairs = DblCur.ExportPair('hash', 'idt')
                for Rec in aDbl:
                    Idt = Pairs.get(ToHashW(Rec.name))
                    Rec.SetField('id', Idt)

            print('SProduct()', aIdx, aLen)
            if (self.Conf.idt_auto):
                await SetAutoIdt()

            Uniq = {}
            Values = []
            Idts = []
            for Rec in aDbl:
                Idt = Rec.GetField('id')
                Key = (Idt, self.tenant_id)
                if (Key not in Uniq):
                    Uniq[Key] = ''
                    Idts.append(Idt)

                    Value = f"({Idt}, {self.tenant_id}, ({Rec.qty} > 0), {bool(Rec.used)}, '{Rec.code}')"
                    Values.append(Value)

            if (Values):
                # Query = f'''
                #     insert into ref_product (idt, tenant_id, enabled, model)
                #     values {', '.join(Values)}
                #     on conflict (idt, tenant_id) do update
                #     set enabled = excluded.enabled, model = excluded.model
                #     returning id, idt
                # '''
                Query = f'''
                    with src (idt, tenant_id, enabled, used, model) as (
                        values {', '.join(Values)}
                    )
                    merge into ref_product as dst
                    using src
                    on (dst.idt = src.idt) and (dst.tenant_id = src.tenant_id)
                    when matched then
                        update set enabled = src.enabled, used = src.used, model = src.model
                    when not matched then
                        insert (idt, tenant_id, enabled, used, model)
                        values (src.idt, src.tenant_id, src.enabled, src.used, src.model)
                '''
                await TDbExecPool(self.Db.Pool).Exec(Query)

                Query = f'''
                    select id, idt
                    from ref_product
                    where (tenant_id = {self.tenant_id}) and (idt in ({ListIntToComma(Idts)}))
                '''
                Res = await TDbExecPool(self.Db.Pool).Exec(Query)
                return Res

        @DASplitDbl
        async def SProduct_Product0(aDbl: TDbProductEx, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct_Product0()', aIdx, aLen)

            Codes = aDbl.ExportList('code')
            if (self.Conf.product0 == 'model'):
                SubQuery =  f'''
                    select
                        rp.id as product_id,
                        rpp.product0_id
                    from
                        ref_product rp
                    left join
                        ref_product_product0 rpp on
                        (rpp.tenant_id = {self.tenant_id}) and (rpp.product_en = 'model') and (rpp.code = rp.model)
                    where
                        (rp.enabled) and
                        (rp.model is not null) and
                        (rp.tenant_id = {self.tenant_id}) and
                        (rp.model in ({ListToComma(Codes)})) and
                        (rpp.enabled) and
                        (rpp.code is not null)

                '''
            elif (self.Conf.product0 == 'ean'):
                SubQuery = f'''
                    select
                        rpb.product_id,
                        rpb0.product_id as product0_id
                    from
                        ref_product_barcode rpb
                    left join
                        ref_product0_barcode rpb0 on
                        (rpb.code = rpb0.code) and (rpb.product_en = rpb.product_en)
                    where
                        (rpb.tenant_id = {self.tenant_id}) and
                        (rpb.code in ({ListToComma(Codes)}))
                '''
            else:
                raise ValueError(f'{self.Conf.product0}')

            Query = f'''
                with wrp as (
                    {SubQuery}
                )
                update
                    ref_product rp
                set
                    product0_id = subquery.product_id
                from (
                    select
                        product_id,
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
                Key = (self.ProductIdt[Rec.id], self.lang_id)
                if (Key not in Uniq):
                    Uniq[Key] = ''

                    Descr = Rec.GetField('descr', '').translate(self.Escape)

                    Features = Rec.GetField('features')
                    if (Features):
                        Features = "'" + json.dumps(Features, ensure_ascii=False).replace("'", '`') + "'"
                    else:
                        Features = 'null'

                    Value = f"({self.ProductIdt[Rec.id]}, {self.lang_id}, '{Rec.name.translate(self.Escape)}', '{Descr}', {Features})"
                    Values.append(Value)

            # no serial column
            Query = f'''
                insert into ref_product_lang (product_id, lang_id, title, descr, features)
                values {', '.join(Values)}
                on conflict (product_id, lang_id) do update
                set title = excluded.title, features = excluded.features, descr = excluded.descr
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

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
                select product_id, image, src_url, src_size
                from ref_product_image
                where (product_id in ({ListIntToComma(ProductIds)}))
            '''
            DblCur = await TDbExecPool(self.Db.Pool).Exec(Query)
            Urls = DblCur.ExportPair('src_url', 'src_size')

            UrlD = []
            for x in Data:
                Url = x['src_url']
                File = Url.rsplit('/', maxsplit=1)[-1]
                Name = f'{self.tenant_id}/{File[:2]}/{File}'
                UrlD.append([Url, Name, Urls.get(Url, 0), x['product_id']])

            DataImg = await self._ImgUpdate(
                {
                    'method': 'UploadUrls',
                    'param': {
                        'aUrlD': UrlD,
                        'aDir': 'product',
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

                # Query = f'''
                #     insert into ref_product_image (product_id, image, src_url, src_size, src_date)
                #     values {', '.join(Values)}
                #     on conflict (product_id, image) do update
                #     set enabled = true, src_size = excluded.src_size, src_date = excluded.src_date
                #     returning id
                # '''
                Query = f'''
                    with src (product_id, image, src_url, src_size, src_date) as (
                        values {', '.join(Values)}
                    )
                    merge into ref_product_image as dst
                    using src
                    on (dst.product_id = src.product_id) and (dst.image = src.image)
                    when matched then
                        update set enabled = true, src_size = src.src_size, src_date = src.src_date
                    when not matched then
                        insert (product_id, image, src_url, src_size, src_date)
                        values (src.product_id, src.image, src.src_url, src.src_size, src.src_date)
                '''
                await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplitDbl
        async def SProduct_ToCategory(aDbl: TDbProductEx, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct_ToCategory()', aIdx, aLen)

            Values = ListIntToComma(aDbl.ExportList('id'))
            Query = f'''
                select
                    idt as product_idt,
                    category_idt
                from
                    ref_product_idt
                where
                    (tenant_id = {self.tenant_id}) and
                    (idt in ({Values})) and
                    (category_idt is not null)
            '''
            Dbl = await TDbExecPool(self.Db.Pool).Exec(Query)

            IdtPairs = Dbl.ExportPair('product_idt', 'category_idt')
            Values = []
            for Rec in aDbl:
                CategoryIdt = IdtPairs.get(Rec.id, Rec.category_id)
                Values.append(f'({self.ProductIdt[Rec.id]}, {self.CategoryIdt[CategoryIdt]})')

            # no serial column
            Query = f'''
                insert into ref_product_to_category (product_id, category_id)
                values {', '.join(Values)}
                on conflict (product_id, category_id) do nothing
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplitDbl
        async def SProduct_Price(aDbl: TDbProductEx, _aMax: int, aIdx: int = 0, aLen: int = 0):
            print('SProduct_Price()', aIdx, aLen)

            ProductIds = []
            for Rec in aDbl:
                ProductIds.append(self.ProductIdt[Rec.id])
            ProductsMargin = await self.GetProductsMargin(ProductIds)

            Values = []
            for Rec in aDbl:
                ProductId = self.ProductIdt[Rec.id]
                Margin = ProductsMargin.get(ProductId, 1)
                if (Rec.price_in):
                    Price = Rec.price_in if (self.CurrencyRate == 1) else int(float(Rec.price_in) / self.CurrencyRate)
                    Value = f'({ProductId}, {self.price_purchase_id}, {Price})'
                    Values.append(Value)

                    if (self.Conf.price_auto) and (not Rec.price):
                        Price = RoundNear(Price * Margin, self.Conf.price_round)
                        Value = f'({ProductId}, {self.price_sale_id}, {Price})'
                        Values.append(Value)

                if (Rec.price):
                    Price = Rec.price if (self.CurrencyRate == 1) else int(float(Rec.price * Margin) / self.CurrencyRate)
                    Value = f'({ProductId}, {self.price_sale_id}, {Price})'
                    Values.append(Value)

            if (Values):
                Query = f'''
                    with src (product_id, price_id, price) as (
                        values {', '.join(Values)}
                    )
                    merge into ref_product_price as dst
                    using src
                    on (dst.product_id = src.product_id) and (dst.price_id = src.price_id) and (dst.qty = 1)
                    when matched and (manual is null or manual = false) then
                        update set price = src.price
                    when not matched then
                        insert (product_id, price_id, price)
                        values (src.product_id, src.price_id, src.price)
                '''
                await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplitDbl
        async def SProduct_Stock(aDbl: TDbProductEx, _aMax: int, aIdx: int = 0, aLen: int = 0):
            print('SProduct_Stock()', aIdx, aLen)

            Ids = []
            Qtys = []
            for Rec in aDbl:
                Ids.append(self.ProductIdt[Rec.id])
                Qtys.append(Rec.qty)

            Query = f'''
                select *
                from
                    stock_set(
                        ARRAY[{ListIntToComma(Ids)}],
                        ARRAY[{ListIntToComma(Qtys)}],
                        {self.stock_id},
                        'doc_rest'
            	)
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplitDbl
        async def SProduct_Barcode(aDbl: TDbProductEx, _aMax: int, aIdx: int = 0, aLen: int = 0) -> TDbList:
            print('SProduct_Barcode()', aIdx, aLen)

            Uniq = {}
            Values = []
            for Rec in aDbl:
                Key = Rec.code
                if (Key):
                    if (Key not in Uniq):
                        Uniq[Key] = ''
                        Value = f"('{Rec.code}', 'ean', {self.ProductIdt[Rec.id]}, {self.tenant_id})"
                        Values.append(Value)
                    else:
                        Log.Print(1, 'i', f'SProduct_Barcode(). Not uniq code: {Rec.code}, id: {Rec.id}, name: {Rec.name}')

            # no serial column
            Query = f'''
                insert into ref_product_barcode (code, product_en, product_id, tenant_id)
                values {', '.join(Values)}
                on conflict (tenant_id, code, product_en) do update
                set product_id = excluded.product_id
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        Log.Print(1, 'i', 'Product')
        await self.DisableTable('ref_product')
        await Product(aDbl)
        aDbl = GetUnique(aDbl)

        Log.Print(1, 'i', 'Product_Price')
        await SProduct_Price(aDbl, self.Conf.parts)

        Log.Print(1, 'i', 'Product_Stock')
        await SProduct_Stock(aDbl, self.Conf.parts)

        if (self.Conf.product0 == 'ean'):
            Log.Print(1, 'i', 'Product_Barcode')
            await SProduct_Barcode(aDbl, self.Conf.parts)

        Log.Print(1, 'i', 'Product_Product0')
        await SProduct_Product0(aDbl, self.Conf.parts)

        Log.Print(1, 'i', 'Product_Lang')
        await SProduct_Lang(aDbl, self.Conf.parts)

        Log.Print(1, 'i', 'Product_ToCategory')
        await SProduct_ToCategory(aDbl, self.Conf.parts)

        Log.Print(1, 'i', 'Product_Image')
        await self.DisableTableByProduct('ref_product_image', 'and (src_url is not null)')
        await SProduct_Image(aDbl, self.Conf.parts)


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
        await self.Sql.LoadTenantConf(self.Sql.Conf.tenant, self.Sql.Conf.lang)
        await self.Sql.GetCurrencyRate()

        Data = TCatalogToDb(aDbCategory).Get()
        await self.Sql.Category_Create(Data)
        await self.Sql.Product_Create(aDbProductEx)
