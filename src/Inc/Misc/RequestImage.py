# Created: 2022.10.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import aiohttp
#
from Inc.Misc.Image import TImage
from .Request import TDownloadBase


class TDownloadImage(TDownloadBase):
    def __init__(self, aDir: str, aMaxSize: int = 1024, aMaxConn: int = 5):
        super().__init__(aMaxConn)
        self.Dir = aDir
        self.MaxSize = aMaxSize
        self.Download = True

    def _GetDir(self, aId: int) -> str:
        # Last = '/'.join(reversed(str(aId)[-2:]))
        # return f'{self.Dir}/{Last}'
        return self.Dir

    async def _DoFetch(self, aUrlD, aResponse: aiohttp.ClientResponse):
        aUrl, aSaveAs, aSize, aImageId = aUrlD

        if (not aSaveAs):
            aSaveAs = aUrl.rsplit('/', maxsplit=1)[-1]
        File = self._GetDir(aImageId) + '/' + aSaveAs

        FileOk = os.path.isfile(File)
        if (aSize == 0 and FileOk):
            aSize = os.path.getsize(File)

        if (self.Download) and ((not FileOk) or (aSize != aResponse.content_length)):
            Dir = File.rsplit('/', maxsplit=1)[0]
            os.makedirs(Dir, exist_ok=True)
            Data = await aResponse.read()
            if (self.MaxSize):
                TImage.ResizeImg(Data, File, self.MaxSize)
            else:
                self._FileWrite(File, Data)

    async def Get(self, aUrls: list[str]) -> list[tuple]:
        Len = len(aUrls)
        Data = zip(aUrls, [0] * Len, [''] * Len)
        return await self.Fetch(Data)
