# Created: 2023.12.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import base64
import json
#
import IncP.LibCtrl as Lib

ImgPrefix = 'product'

async def ajax(self, aData: dict = None) -> dict:
    aLang, aPath, Mode = Lib.GetDictDefs(
        aData.get('query'),
        ('lang', 'path', 'mode'),
        ('ua', '', 'list')
    )
    AuthId = Lib.DeepGetByList(aData, ['session', 'auth_id'])
    Path = f'{ImgPrefix}/{AuthId}'
    Dir = f'{Path}/{aPath}'.rstrip('/')
    Post = aData.get('post', {})
    await DoPost(self, Post, AuthId, Dir)


async def DoPost(self, aPost, aAuthId, aDir) -> dict:
    if (aPost.get('new_folder')):
        DirNew = (aDir + '/' + aPost.get('new_folder')).lstrip('/')
        await self.ExecImg(
            'system',
            {
                'method': 'CreateDirs',
                'param': {'aPaths': [DirNew]}
            }
        )

    if (aPost.get('btn_delete')):
        ChkItems = Lib.DeepGetsRe(aPost, ['chk_(file|folder)_.*'])
        Items = [f'{ImgPrefix}/{x[0]}' for x in ChkItems]
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
                Items.append(File.replace(ImgPrefix + '/', ''))

            await self.ExecModel(
                'ref_product/product',
                {
                    'method': 'Del_TenantImages',
                    'param': {
                        'aTenantId': aAuthId,
                        'aImages': Items
                    }
                }
            )

    if (aPost.get('btn_upload')) and ('files' in aPost):
        Data = {}
        for Key, Val in aPost['files'].items():
            Base64 = base64.b64encode(Val).decode('utf-8')
            Data[Key] = json.dumps(Base64)

        await self.ExecImg(
            'system',
            {
                'method': 'UploadFiles',
                'param': {
                    'aPath': aDir,
                    'aFiles': Data
                }
            }
        )

async def Main(self, aData: dict = None) -> dict:
    # - entry -
    aLang, aPath, Mode = Lib.GetDictDefs(
        aData.get('query'),
        ('lang', 'path', 'mode'),
        ('ua', '', 'list')
    )

    AuthId = Lib.DeepGetByList(aData, ['session', 'auth_id'])
    Path = f'product/{AuthId}'
    Dir = f'{Path}/{aPath}'.rstrip('/')

    if (aData.get('post')):
        Post = aData.get('post')
        await DoPost(self, Post, AuthId, Dir)

    DblData = await self.ExecImg(
        'system',
        {
            'method': 'GetDirList',
            'param': {'aPath': Dir}
        }
    )

    if (DblData):
        Dbl = Lib.TDbList().Import(DblData)
        for Rec in Dbl:
            if (Rec.type == 'd'):
                Arr = Rec.href.rsplit(Path, maxsplit=1)
                Dir = Arr[1].lstrip('/')
                Rec.SetField('href', f"/tenant/?route={aData['route']}&path={Dir}")
            Rec.SetField('path', Rec.path.replace(ImgPrefix + '/' ,''))

        Arr = aPath.rsplit('/', maxsplit=1)
        Parent = '' if len(Arr) == 1 else Arr[0]

        Res = {
            'dbl_dirlist': Dbl.Export(),
            'href': {
                'parent': f"/tenant/?route={aData['route']}&path={Parent}",
                'refresh': aData['path_qs']
            }
        }
        return Res
