# Created: 2023.12.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import  DeepGetByList, GetDictDefs, TDbList


async def Main(self, aData: dict = None) -> dict:
    aPath, Mode = GetDictDefs(
        aData.get('query'),
        ('path', 'mode'),
        ('', 'list')
    )
    AuthId = DeepGetByList(aData, ['session', 'auth_id'])

    Path = f'product/{AuthId}'
    DblData = await self.ExecImg(
        'system',
        {
            'method': 'GetDirList',
            'param': {'aPath': f'{Path}/{aPath}'}
        }
    )

    if (DblData):
        Dbl = TDbList().Import(DblData)
        for Rec in Dbl:
            if (Rec.type == 'd'):
                Arr = Rec.href.rsplit(Path, maxsplit=1)
                Dir = Arr[1].lstrip('/')
                Rec.SetField('href', f'/tenant/?route=common/filemanager&path={Dir}')

        Arr = aPath.rsplit('/', maxsplit=1)
        Parent = '' if len(Arr) == 1 else Arr[0]

        Res = {
            'dbl_dirlist': Dbl.Export(),
            'href': {
                'parent': f'/tenant/?route=common/filemanager&path={Parent}',
                'refresh': aData['path_qs']
            }
        }
        return Res
