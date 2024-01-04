# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import time
import base64
#
from Inc.Misc.FS import DirRemove
from IncP.LibCtrl import TDownload, TDownloadImage, TImage, TDbList


def _GetImagesInfo(self, aFiles: list[str]) -> TDbList:
    Dbl = TDbList(['name', 'type', 'size', 'date', 'href', 'path'])
    for xFile in aFiles:
        Path = f'{self.Conf.dir_root}/{xFile}'
        if (os.path.exists(Path)):
            Type = 'd' if (os.path.isdir(Path)) else 'f'
            Stat = os.stat(Path)
            Size = Stat.st_size
            Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(Stat.st_mtime))
            Href = f'{self.Conf.url}/{xFile}'
        else:
            Type = None
            Size = -1
            Time = 0
            Href = f'{self.Conf.url}/{self.Conf.no_image}'
        File = xFile.rsplit('/', maxsplit=1)[-1]
        Dbl.RecAdd([File, Type, Size, Time, Href, xFile])
    return Dbl

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

async def GetImagesInfo(self, aFiles: list[str]) -> TDbList:
    return _GetImagesInfo(self, aFiles)

async def GetDirList(self, aPath: str) -> dict:
    Dir = f'{self.Conf.dir_root}/{aPath}'
    Files = [f'{aPath}/{File}' for File in os.listdir(Dir)]
    Dbl = _GetImagesInfo(self, Files)
    return Dbl.Sort(['type', 'name']).Export()

async def CreateDirs(self, aPaths: list[str]):
    for xPath in aPaths:
        Path = f'{self.Conf.dir_root}/{xPath}'
        os.makedirs(Path, exist_ok=True)

async def Remove(self, aPaths: list[str]) -> list[str]:
    Res = []
    for xPath in aPaths:
        Path = f'{self.Conf.dir_root}/{xPath}'
        if (os.path.isdir(Path)):
            Res += DirRemove(Path)
        else:
            os.remove(Path)
            Res.append(Path)
    return {'files': Res}

async def Upload(self, aPath: str, aFiles: dict) -> list[str]:
    Res = []
    for Key, Val in aFiles.items():
        Path = f'{self.Conf.dir_root}/{aPath}/{Key}'
        Data = base64.b64decode(Val)
        with open(Path, 'wb') as F:
            F.write(Data)
        Res.append(Path)
    return {'files': Res}
