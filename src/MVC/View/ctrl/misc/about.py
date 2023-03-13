# Created: 2022.02.14
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP import LibView
from IncP.LibView import TFormBase, GetTree, GetInfo


class TForm(TFormBase):
    def _DoInit(self):
        #self.out.title = 'About'
        pass

    async def _DoRender(self):
        self.out.title = 'view/ctrl/misc/about.py'
        self.out.MyData = 'Pink Floyd'

        LibInfo = [x for x in dir(LibView) if not x.startswith('_')]
        LibInfo = sorted(LibInfo)

        Data = await self.ExecCtrlDef()
        DbInfo = []
        for Complex, Path, Obj, _Depth in GetTree(Data):
            if (not Complex):
                DbInfo.append(f'{Path}: {Obj}')
        DbInfo = sorted(DbInfo)

        Data = GetInfo()
        Info = []
        for Complex, Path, Obj, _Depth in GetTree(Data):
            if (not Complex):
                Info.append(f'{Path}: {Obj}')
        Info = sorted(Info)

        ReqInfo = [
            f'host: {self.Request.host}',
            f'remote: {self.Request.remote}'
        ]

        Res = DbInfo + [''] + ReqInfo + [''] + Info + [''] + LibInfo
        self.out.data['info'] = '<br>\n'.join(Res)
