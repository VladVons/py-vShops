# Created: 2023.03.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.Sql import TDbPg, TDbExecPool


class TLoaderQuery():
    def __init__(self, aParent):
        self.Parent = aParent
        Path = aParent.__module__.replace('.', '/')
        if (not os.path.isdir(Path)):
            Path = Path.rsplit('/', maxsplit = 1)[0]
        assert(os.path.isdir(Path)), f'Directory not exists {Path}'
        self.Path = Path

    async def Get(self, aName: str, aValues: dict) -> str:
        raise NotImplementedError()


class TLoaderQueryFs(TLoaderQuery):
    async def Get(self, aName: str, aValues: dict) -> str:
        File = f'{self.Path}/{aName}'
        return self.Parent.ApiModel.Env.get_template(File).render(aValues)


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
