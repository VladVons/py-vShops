# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
import re
import os
#
from Inc.DataClass import DDataClass
from Inc.DbList import TDbList
from Inc.Log import TLog, TEchoFile
from Inc.Misc.Template import FormatFile
from Inc.Sql import TDbExecPool, TDbPg
from Inc.Util.Arr import Parts


@DDataClass
class TSqlTenantConf():
    lang: str
    tenant: str
    parts: int = 100


def StripQuery(aData: str) -> str:
    return re.sub(r'\s+', ' ', aData).strip()

def DSplit(aFunc: callable) -> list[str]:
    def Decor(aData: list, aMax: int) -> list[str]:
        Res = []
        for Part in Parts(aData, aMax):
            Data = aFunc(Part, aMax)
            Res.append(StripQuery(Data).strip())
        return Res
    return Decor

def DASplit(aFunc: callable) -> list[str]:
    async def Decor(aData: list, aMax: int) -> list[str]:
        Res = []
        Len = len(aData) // aMax
        for Idx, Part in enumerate(Parts(aData, aMax)):
            Data = await aFunc(Part, aMax, Idx, Len)
            Res.append(Data)
        return Res
    return Decor

def DASplitDbl(aFunc: callable) -> list:
    async def Decor(aDbl: TDbList, aMax: int) -> list:
        Res = []
        Len = aDbl.GetSize() // aMax
        for Idx, Part in enumerate(Parts(aDbl.Data, aMax)):
            Dbl = aDbl.New(Part)
            Data = await aFunc(Dbl, aMax, Idx, Len)
            Res.append(Data)
        return Res
    return Decor


class TLogEx(TLog):
    def Write(self, aData):
        self._Write({'aM': aData}, [])

    def Init(self, aFile: str):
        if (os.path.exists(aFile)):
            os.remove(aFile)
        else:
            os.makedirs(os.path.dirname(aFile), exist_ok=True)

        EchoFile = TEchoFile(aFile)
        EchoFile.Fmt = ['aM']
        return TLogEx([EchoFile])


class TSqlBase():
    def __init__(self, aDb: TDbPg):
        self.Db = aDb
        self.Now = time.strftime('%Y-%m-%d %H:%M:%S')
        self.Escape = ''.maketrans({
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            "'": '&apos;',
            '"': '&quot;'
            })

        self.lang_id: int
        self.tenant_id: int
        self.price_sale_id: int
        self.price_purchase_id: int
        self.stock_id: int

    async def ExecQuery(self, aPackage: str, aFile: str, aFormat: dict = None) -> TDbList:
        Dir = aPackage.replace('.', '/')
        Query = FormatFile(f'{Dir}/{aFile}', aFormat or {})
        return await TDbExecPool(self.Db.Pool).Exec(Query)

    async def LoadTenantConf(self, aTenant: str, aLang: str):
        Query = f'''
            select
                rt.id as tenant_id,
                (select id from ref_lang where alias = '{aLang}') as lang_id,
                (select id from ref_stock where tenant_id = rt.id and idt = 1) as stock_id,
                (select id from ref_price where tenant_id = rt.id and price_en = 'sale') as price_sale_id,
                (select id from ref_price where tenant_id = rt.id and price_en = 'purchase') as price_purchase_id
            from
                ref_tenant rt
            where
                (rt.enabled) and (rt.alias = '{aTenant}')
        '''
        Dbl = await TDbExecPool(self.Db.Pool).Exec(Query)
        assert(not Dbl.IsEmpty()), f'No tenant alias found or disabled {aTenant}'

        for Field in Dbl.Rec:
            assert(Dbl.Rec.GetField(Field)), f'Empty field {Field}'

        self.tenant_id = Dbl.Rec.tenant_id
        self.lang_id = Dbl.Rec.lang_id
        self.price_sale_id = Dbl.Rec.price_sale_id
        self.price_purchase_id = Dbl.Rec.price_purchase_id
        self.stock_id = Dbl.Rec.stock_id

    async def LoadLang(self, aLang: str):
        Query = f'''
            select id
            from ref_lang
            where (alias = '{aLang}')
        '''
        Dbl = await TDbExecPool(self.Db.Pool).Exec(Query)
        self.lang_id = Dbl.Rec.id
