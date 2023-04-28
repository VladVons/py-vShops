# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.Misc.Request import TDownload, TDownloadImage
from Inc.Misc.Image import TImage


async def UploadUrl(self, aUrl: str, aFile: str) -> dict:
    Path, File = aFile.rsplit('/', maxsplit = 1)
    Download = TDownload(f'{self.Conf.dir_root}/{Path}')
    Res = await Download.Get([aUrl], [File])
    return {'status': Res}

async def UploadUrls(self, aUrlD: list, aDir: str, aDownload: bool = True) -> dict:
    Download = TDownloadImage(f'{self.Conf.dir_root}/{aDir}', self.Conf.size_product)
    Download.Download = aDownload
    Res = await Download.Fetch(aUrlD)
    return {'status': Res}

async def GetThumbs(self, aFiles: list[str]) -> dict:
    Res = []
    for x in aFiles:
        Thumb = f'{self.Conf.url}/{self.Conf.dir_thumb}/{x}'
        FileOut = f'{self.Conf.dir_root}/{self.Conf.dir_thumb}/{x}'
        if (not os.path.isfile(FileOut)):
            FileIn = f'{self.Conf.dir_root}/{x}'
            if (os.path.isfile(FileIn)):
                Path, _File = x.rsplit('/', maxsplit = 1)
                PathOut = f'{self.Conf.dir_root}/{self.Conf.dir_thumb}/{Path}'
                os.makedirs(PathOut, exist_ok = True)
                TImage.ResizeFile(FileIn, FileOut, self.Conf.size_thumb)
            else:
                Thumb = ''
        Res.append(Thumb)
    return  {'thumb': Res}

async def GetImages(self, aFiles: list[str]) -> dict:
    Res = []
    for x in aFiles:
        File = f'{self.Conf.dir_root}/{x}'
        if (os.path.isfile(File)):
            Image = f'{self.Conf.url}/{x}'
            Res.append(Image)
    return {'image': Res}

async def Remove(self, aFiles: list[str]) -> dict:
    Dirs = [self.Conf.dir_root, f'{self.Conf.dir_root}/{self.Conf.dir_thumb}']
    for Dir in Dirs:
        for File in aFiles:
            File = f'{Dir}/{File}'
            if (os.path.exists(File)):
                os.remove(File)
    return {}
