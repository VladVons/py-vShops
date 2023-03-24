# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from Inc.DbList  import TDbList, TDbRec
from Inc.DataClass import DDataClass
from Inc.ParserX.Common import TFileBase
from Inc.ParserX.CommonSql import TSqlBase, DASplit, TLogEx
from Inc.Sql.DbPg import TDbPg
from Inc.Sql.ADb import TDbExecPool, ListIntToComma
from IncP.Log import Log
from ..CommonDb import TDbCategory, TDbProductEx


@DDataClass
class TSqlConf():
    LangId: int
    TenantId: int
    PriceId: int
    Parts: int = 100
    DirImage: str = 'catalog/products'


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
    def __init__(self, aDb: TDbPg, aSqlConf: TSqlConf):
        super().__init__()

        self.Db = aDb
        self.Conf = aSqlConf
        self.CategoryIdt = {}
        self.ProductIdt = {}

    async def Product_Clear(self):
        Query = f'''
            delete from ref_product_image
            where product_id in (
                select id
                from ref_product
                where tenant_id = {self.Conf.TenantId}
            )
            ;
        '''
        await TDbExecPool(self.Db.Pool).Exec(Query)

        Query = f'''
            delete from ref_product_to_category
            where product_id in (
                select id
                from ref_product
                where tenant_id = {self.Conf.TenantId}
            )
            ;
        '''
        await TDbExecPool(self.Db.Pool).Exec(Query)

    async def Category_Create(self, aData: list):
        async def Category(aData: list):
            Dbls: list[TDbList] = await _Category(aData, self.Conf.Parts)
            Dbl = Dbls[0].New()
            Dbl.Append(Dbls)
            self.CategoryIdt = Dbl.ExportPair('idt', 'id')

        @DASplit
        async def _Category(aData: list, _aMax: int) -> TDbList:
            Values = [f"({Row['id']}, {Row['parent_id']}, {self.Conf.TenantId})" for Row in aData]
            Query = f'''
                insert into ref_product_category (idt, parent_idt, tenant_id)
                values {', '.join(Values)}
                on conflict (idt, tenant_id) do nothing
                returning (id, idt)
                ;
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

            Ids = [Row['id'] for Row in aData]
            Query = f'''
                select
                    id, idt
                from
                    ref_product_category
                where
                    idt in ({ListIntToComma(Ids)})
                ;
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplit
        async def Category_Lang(aData: list, _aMax: int) -> TDbList:
            Values = [
                f"({self.CategoryIdt[Row['id']]}, {self.Conf.LangId}, '{Row['name'].translate(self.Escape)}')"
                for Row in aData
            ]
            Query = f'''
                insert into ref_product_category_lang (category_id, lang_id, title)
                values {', '.join(Values)}
                on conflict (category_id, lang_id) do update
                set title = excluded.title
                ;
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

        Log.Print(1, 'i', 'Category')
        await Category(aData)
        Log.Print(1, 'i', 'Category_Lang')
        await Category_Lang(aData, self.Conf.Parts)

    async def Product_Create(self, aDbl: TDbProductEx):
        async def Product(aData: list):
            Dbls: list[TDbList] = await _Product(aData, self.Conf.Parts)
            Dbl = Dbls[0].New()
            Dbl.Append(Dbls)
            self.ProductIdt = Dbl.ExportPair('idt', 'id')

        @DASplit
        async def _Product(aData: list, _aMax: int) -> TDbList:
            nonlocal DbRec

            Ids = []
            Values = []
            for Row in aData:
                DbRec.Data = Row
                Id = DbRec.GetField('id')

                Value = f'({Id}, {self.Conf.TenantId}, {bool(DbRec.available)})'
                Values.append(Value)
                Ids.append(Id)

            Query = f'''
                insert into ref_product (idt, tenant_id, enabled)
                values {', '.join(Values)}
                on conflict (idt, tenant_id) do update
                set enabled = excluded.enabled
                ;
            '''
            await TDbExecPool(self.Db.Pool).Exec(Query)

            Query = f'''
                select
                    id, idt
                from
                    ref_product
                where
                    idt in ({ListIntToComma(Ids)})
                ;
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplit
        async def Product_Lang(aData: list, _aMax: int) -> TDbList:
            nonlocal DbRec

            Values = []
            for Row in aData:
                DbRec.Data = Row
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
                ;
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplit
        async def Product_Image(aData: list, _aMax: int) -> TDbList:
            nonlocal DbRec

            Values = []
            for Row in aData:
                DbRec.Data = Row
                for xImage in DbRec.GetField('image', []):
                    Image = xImage.split('/')[-1]
                    Value = f"({self.ProductIdt[DbRec.id]}, '{Image}')"
                    Values.append(Value)

            Query = f'''
                insert into ref_product_image (product_id, image)
                values {', '.join(Values)}
                ;
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplit
        async def Product_ToCategory(aData: list, _aMax: int) -> TDbList:
            nonlocal DbRec

            Values = []
            for Row in aData:
                DbRec.Data = Row
                Values.append(f'({self.ProductIdt[DbRec.id]}, {self.CategoryIdt[DbRec.category_id]})')

            Query = f'''
                insert into ref_product_to_category (product_id, category_id)
                values {', '.join(Values)}
                ;
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)

        @DASplit
        async def Product_Price(aData: list, _aMax: int) -> TDbList:
            nonlocal DbRec

            Values = []
            for Row in aData:
                DbRec.Data = Row
                Value = f'({self.ProductIdt[DbRec.id]}, {self.Conf.PriceId}, {DbRec.price})'
                Values.append(Value)

            Query = f'''
                insert into ref_product_price (product_id, price_id, price)
                values {', '.join(Values)}
                on conflict (product_id, price_id, qty) do update
                set price = excluded.price
                ;
            '''
            return await TDbExecPool(self.Db.Pool).Exec(Query)


        DbRec = TDbRec()
        DbRec.Fields = aDbl.Rec.Fields

        Log.Print(1, 'i', 'Product')
        await Product(aDbl.Data)
        Log.Print(1, 'i', 'Product_Lang')
        await Product_Lang(aDbl.Data, self.Conf.Parts)
        Log.Print(1, 'i', 'Product_Image')
        await Product_Image(aDbl.Data, self.Conf.Parts)
        Log.Print(1, 'i', 'Product_ToCategory')
        await Product_ToCategory(aDbl.Data, self.Conf.Parts)
        Log.Print(1, 'i', 'Product_Price')
        await Product_Price(aDbl.Data, self.Conf.Parts)


class TMain(TFileBase):
    def __init__(self, aParent, aDb: TDbPg):
        super().__init__(aParent)

        ConfFile = self.Parent.GetFile()
        self.LogEx = TLogEx()
        self.LogEx = self.LogEx.Init(ConfFile)

        SqlDef = self.Parent.Conf.GetKey('sql', {})
        SqlConf = TSqlConf(
            DirImage = self.Parent.Conf.GetKey('site_image'),
            TenantId = SqlDef.get('tenant_id'),
            LangId = SqlDef.get('lang_id'),
            PriceId = SqlDef.get('price_id'),
            Parts = SqlDef.get('parts', 50)
        )
        self.Sql = TSql(aDb, SqlConf)

    async def InsertToDb(self, aDbCategory: TDbCategory, aDbProductEx: TDbProductEx):
        Data = TCatalogToDb(aDbCategory).Get()
        await self.Sql.Category_Create(Data)
        await self.Sql.Product_Clear()
        await self.Sql.Product_Create(aDbProductEx)
