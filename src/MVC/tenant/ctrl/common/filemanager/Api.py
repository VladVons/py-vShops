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
            Items = DeepGetsRe(Post, ['chk_.*'])
            Items = [x[0] for x in Items]
            if (Items):
                await self.ExecImg(
                    'system',
                    {
                        'method': 'Remove',
                        'param': {'aPaths': Items}
                    }
                )

                ItemsBase = [x.replace('product/', '') for x in Items]
                await self.ExecModel(
                    'ref_product/product',
                    {
                        'method': 'Del_TenantImages',
                        'param': {'aTenantId': AuthId, 'aImages': ItemsBase}
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
                    'method': 'Upload',
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
