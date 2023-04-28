# Created: 2022.10.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import time
import asyncio
import aiohttp
#
from Inc.Misc.Image import TImage


_Excepts = (aiohttp.ClientConnectorError, aiohttp.ClientError, aiohttp.InvalidURL, asyncio.TimeoutError)

class TRecSes():
    def __init__(self, aUrl: str, aDataSend = None, aDataUser = None, aOnRead: callable = None):
        self.Url = aUrl
        self.DataSend = aDataSend
        self.DataUser = aDataUser
        self.TaskNo = 0
        self.OnRead = aOnRead


class TAuth():
    def __init__(self, aUser: str, aPassw: str):
        self.User = aUser
        self.Passw = aPassw
        self.Hash = self.Get()

    def Get(self) -> aiohttp.BasicAuth:
        return aiohttp.BasicAuth(login=self.User, password=self.Passw)


class TRequest():
    def __init__(self, aBaseUrl: str = None, aAuth: TAuth = None, aCallBack = None):
        self.CallBack: callable = aCallBack
        self.Sleep = 0
        Auth = aAuth.Hash if (aAuth) else None
        self.Session = aiohttp.ClientSession(base_url=aBaseUrl, auth=Auth)

    async def Close(self):
        await self.Session.close()

    async def _SendRec(self, aRecSes: TRecSes) -> dict:
        raise NotImplementedError()

    async def _SendSem(self, aSem: asyncio.Semaphore, aRecSes: TRecSes, aTaskNo: int = 0) -> dict:
        async with aSem:
            aRecSes.TaskNo = aTaskNo
            return await self.SendOne(aRecSes)

    async def SendOne(self, aRecSes: TRecSes) -> dict:
        await asyncio.sleep(self.Sleep)
        TimeAt = time.time()
        try:
            Res = await self._SendRec(aRecSes)
            Res['time'] = round(time.time() - TimeAt, 2)
        except _Excepts as E:
            Res = {'err': str(E), 'time': round(time.time() - TimeAt, 2)}
        else:
            if (self.CallBack):
                Res = await self.CallBack(aRecSes, Res)
        return Res

    async def SendMany(self, aTRecSes: list, aMaxTask: int = 5) -> list:
        Sem = asyncio.Semaphore(aMaxTask)
        Tasks = [asyncio.create_task(self._SendSem(Sem, RecSes, Idx)) for Idx, RecSes in enumerate(aTRecSes)]
        return await asyncio.gather(*Tasks)


class TRequestJson(TRequest):
    async def Send(self, aUrl: str, aData: dict) -> dict:
        try:
            async with self.Session.post(aUrl, json=aData) as Response:
                Data = await Response.json()
                Res = {'data': Data, 'status': Response.status}
        except _Excepts as E:
            Res = {'err': str(E)}
        return Res

    async def _SendRec(self, aRecSes: TRecSes) -> dict:
        async with self.Session.post(aRecSes.Url, json=aRecSes.DataSend) as Response:
            Data = await Response.json()
            return {'data': Data, 'status': Response.status}

class TRequestGet(TRequest):
    async def Send(self, aUrl: str) -> dict:
        try:
            async with self.Session.get(aUrl) as Response:
                Data = await Response.read()
                Res = {'data': Data, 'status': Response.status}
        except _Excepts as E:
            Res = {'err': str(E)}
        return Res

    async def _SendRec(self, aRecSes: TRecSes) -> dict:
        async with self.Session.get(aRecSes.Url) as Response:
            if (aRecSes.OnRead):
                Res = await aRecSes.OnRead(aRecSes, Response)
            else:
                Res = await Response.read()
            return {'data': Res, 'status': Response.status}


class TCheckUrls(TRequestGet):
    _Count = 0

    async def _OnSend(self, aRecSes: TRecSes, aResponse: aiohttp.ClientResponse):
        if (aRecSes.TaskNo % 100 == 0):
            print(f'Check {aRecSes.TaskNo:4}/{self._Count}, {aRecSes.Url}')
        #while await aResponse.content.readany()
        return (aResponse.status == 200)

    async def Check(self, aUrls: list, aTasks: int = 5, aSleep: int = 0):
        self._Count = len(aUrls)
        self.Sleep = aSleep
        RecSes = [TRecSes(x, aOnRead=self._OnSend) for x in aUrls]
        Res = await self.SendMany(RecSes, aTasks)
        return Res


class TDownloadBase():
    def __init__(self, aMaxConn: int = 5):
        self.MaxConn = aMaxConn

    async def _FileWrite(self, aFile: str, aData: bytes):
        with open(aFile, 'wb') as F:
            F.write(aData)

    async def _DoFetch(self, aUrlD: tuple, aResponse: aiohttp.ClientResponse):
        raise NotImplementedError()

    async def _Fetch(self, aUrlD: tuple, aSession: aiohttp.ClientSession) -> int:
        '''
        if success returns file size, otherwise negative error code
        '''

        Res = -1
        async with aSession.get(aUrlD[0]) as Response:
            try:
                if (Response.status == 200):
                    Res = Response.content_length
                    await self._DoFetch(aUrlD, Response)
                else:
                    Res = -Response.status
            except Exception:
                pass
        return Res

    async def _FetchSem(self, aUrlD: tuple, aSession: aiohttp.ClientSession, aSem: asyncio.Semaphore) -> list[int]:
        async with aSem:
            return await self._Fetch(aUrlD, aSession)

    async def Fetch(self, aUrlD: list) -> list[int]:
        Sem = asyncio.Semaphore(self.MaxConn)
        async with aiohttp.ClientSession() as Session:
            Tasks = [asyncio.create_task(self._FetchSem(UrlD, Session, Sem)) for UrlD in aUrlD]
            return await asyncio.gather(*Tasks)


class TDownload(TDownloadBase):
    def __init__(self, aDir: str, aMaxConn: int = 5, aForce: bool = False):
        super().__init__(aMaxConn)

        self.Dir = aDir
        self.Force = aForce
        os.makedirs(aDir, exist_ok = True)

    async def _DoFetch(self, aUrlD: tuple, aResponse: aiohttp.ClientResponse):
        Url, SaveAs = aUrlD
        if (not SaveAs):
            SaveAs = Url.rsplit('/', maxsplit=1)[-1]

        File = f'{self.Dir}/{SaveAs}'
        if (not os.path.isfile(File)) or (self.Force) or (os.path.getsize(File) != aResponse.content_length):
            Data = await aResponse.read()
            await self._FileWrite(File, Data)

    async def Get(self, aUrls: list[str], aSaveAs: list = None) -> list[int]:
        if (not aSaveAs):
            aSaveAs = [None] * len(aUrls)
        else:
            assert(len(aUrls) == len(aSaveAs)), 'Size mismatch'
        return await self.Fetch(zip(aUrls, aSaveAs))


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
        aUrl, aSize, aImageId = aUrlD

        Dir = self._GetDir(aImageId).rstrip('/')
        SaveAs = aUrl.rsplit('/', maxsplit=1)[-1]
        File = f'{Dir}/{SaveAs}'

        FileOk = os.path.isfile(File)
        if (aSize == 0 and FileOk):
            aSize = os.path.getsize(File)

        if (self.Download) and ((not FileOk) or (aSize != aResponse.content_length)):
            os.makedirs(Dir, exist_ok=True)
            Data = await aResponse.read()
            if (self.MaxSize):
                TImage.ResizeImg(Data, File, self.MaxSize)
            else:
                self._FileWrite(File, Data)

    async def Get(self, aUrls: list[str]) -> list[int]:
        Len = len(aUrls)
        Data = zip(aUrls, [0] * Len, [''] * Len)
        return await self.Fetch(Data)
