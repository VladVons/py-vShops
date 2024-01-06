# Created: 2023.12.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import base64
import json
#
from IncP.LibCtrl import  DeepGetByList, GetDictDefs, TDbList, DeepGetsRe


async def Main(self, aData: dict = None) -> dict:
    async def DoPost() -> dict:
        nonlocal Path, AuthId
        Post = aData.get('post')

        if (Post.get('new_folder')):
            Dir = (Path + '/' + Post.get('new_folder')).lstrip('/')
            await self.ExecImg(
                'system',
                {
                    'method': 'CreateDirs',
                    'param': {'aPaths': [Dir]}
                }
            )

        if (Post.get('btn_delete')):
            ChkItems = DeepGetsRe(Post, ['chk_(file|folder)_.*'])
            Items = [x[0] for x in ChkItems]
            if (Items):
                await self.ExecImg(
                    'system',
                    {
                        'method': 'RemoveFiles',
                        'param': {'aPaths': Items}
                    }
                )

                Items = []
                for File, Type in ChkItems:
                    if ('folder' in Type):
                        File += '/%'
                    Items.append(File.replace('product/', ''))

                await self.ExecModel(
                    'ref_product/product',
                    {
                        'method': 'Del_TenantImages',
                        'param': {'aTenantId': AuthId, 'aImages': Items}
                    }
                )

        if (Post.get('btn_upload')):
            Data = {}
            for Key, Val in Post['files'].items():
                Base64 = base64.b64encode(Val).decode('utf-8')
                Data[Key] = json.dumps(Base64)

            await self.ExecImg(
                'system',
                {
                    'method': 'UploadFiles',
                    'param': {'aPath': Path, 'aFiles': Data}
                }
            )


    aPath, Mode = GetDictDefs(
        aData.get('query'),
        ('path', 'mode'),
        ('', 'list')
    )
    AuthId = DeepGetByList(aData, ['session', 'auth_id'])
    Path = f'product/{AuthId}'

    if (aData['post']):
        await DoPost()

    Dir = f'{Path}/{aPath}'.rstrip('/')
    DblData = await self.ExecImg(
        'system',
        {
            'method': 'GetDirList',
            'param': {'aPath': Dir}
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
