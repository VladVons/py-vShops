# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
import re
import os
#
from Inc.DbList import TDbList
from Inc.Log import TLog, TEchoFile
from Inc.Misc.Template import FormatFile
from Inc.Sql import TDbExecPool, TDbPg
from Inc.Util.Arr import Parts


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
        self.price_id: int
        self.stock_id: int

    async def ExecQuery(self, aPackage: str, aFile: str, aFormat: dict) -> TDbList:
        Dir = aPackage.replace('.', '/')
        Query = FormatFile(f'{Dir}/{aFile}', aFormat)
        return await TDbExecPool(self.Db.Pool).Exec(Query)

    async def LoadTenantConf(self, aTenant: str, aLang: str):
        Query = f'''
            select
                rt.id as tenant_id,
                rs.id as stock_id,
                rp.id as price_id,
                (select id from ref_lang where alias = '{aLang}') as lang_id
            from
                ref_tenant rt
            left join
                ref_price rp on
                (rt.id = rp.tenant_id) and (rp.idt = 1)
            left join
                ref_stock rs on
                (rt.id = rs.tenant_id) and (rs.idt = 1)
            where
                (rt.enabled) and
                (rt.alias = '{aTenant}')


        '''

        Dbl = await TDbExecPool(self.Db.Pool).Exec(Query)
        assert(not Dbl.IsEmpty()), f'No alias found {aTenant}'

        for Field in Dbl.Rec:
            assert(Dbl.Rec.GetField(Field)), f'Empty field {Field}'

        self.tenant_id = Dbl.Rec.tenant_id
        self.lang_id = Dbl.Rec.lang_id
        self.price_id = Dbl.Rec.price_id
        self.stock_id = Dbl.Rec.stock_id

    async def LoadLang(self, aLang: str):
        Query = f'''
            select id
            from ref_lang
            where (alias = '{aLang}')
        '''
        Dbl = await TDbExecPool(self.Db.Pool).Exec(Query)
        self.lang_id = Dbl.Rec.id
