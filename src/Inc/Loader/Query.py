# Created: 2023.03.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.Misc.Template import FormatFile
from Inc.Sql import TDbPg, TDbExecPool


class TLoaderQuery():
    def __init__(self, aClass: object):
        Path = aClass.__module__.replace('.', '/')
        if (not os.path.isdir(Path)):
            Path = Path.rsplit('/', maxsplit = 1)[0]
        self.Path = Path
        assert (os.path.isdir(Path)), 'Directory not exists'

    async def Get(self, aName: str, aValues: dict) -> str:
        raise NotImplementedError()


class TLoaderQueryFs(TLoaderQuery):
    async def Get(self, aName: str, aValues: dict) -> str:
        return FormatFile(f'{self.Path}/{aName}', aValues)


class TLoaderQueryDb(TLoaderQuery):
    def __init__(self, aClass: object, aDb: TDbPg):
        super().__init__(aClass)
        self.Db = aDb

    async def Get(self, aName: str, aValues: dict) -> str:
        Query = f'''
            select
                query
            from
                ref_query
            where
                (path = '{self.Path}') and
                (title = '{aName}')
        '''
        Dbl = await TDbExecPool(self.Db.Pool).Exec(Query)
        return Dbl.Rec.query.format(**aValues)
