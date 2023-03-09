# Created: 2022.10.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
import asyncio
import aiohttp
#


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
    def __init__(self, aCallBack = None, aAuth: TAuth = None):
        self.CallBack: callable = aCallBack
        self.Auth = aAuth
        self.Sleep = 0

    def _GetAuth(self):
        if (self.Auth):
            return self.Auth.Hash

    async def _Send(self, aSession: aiohttp.ClientSession, aRecSes: TRecSes) -> dict:
        raise NotImplementedError()

    async def _SendSem(self, aSession: aiohttp.ClientSession, aSem: asyncio.Semaphore, aRecSes: TRecSes, aTaskNo: int = 0) -> dict:
        async with aSem:
            aRecSes.TaskNo = aTaskNo
            return await self._SendTry(aSession, aRecSes)

    async def _SendTry(self, aSession: aiohttp.ClientSession, aRecSes: TRecSes) -> dict:
        await asyncio.sleep(self.Sleep)
        TimeAt = time.time()
        try:
            Res = await self._Send(aSession, aRecSes)
            Res['time'] = round(time.time() - TimeAt, 2)
        except (aiohttp.ClientConnectorError, aiohttp.ClientError, aiohttp.InvalidURL, asyncio.TimeoutError) as E:
            Res = {'err': str(E), 'time': round(time.time() - TimeAt, 2)}
        else:
            if (self.CallBack):
                Res = await self.CallBack(aRecSes, Res)
        return Res

    async def SendMany(self, aTRecSes: list, aMaxTask: int = 5) -> list:
        Sem = asyncio.Semaphore(aMaxTask)
        async with aiohttp.ClientSession(auth=self._GetAuth()) as Session:
            Tasks = [asyncio.create_task(self._SendSem(Session, Sem, RecSes, Idx)) for Idx, RecSes in enumerate(aTRecSes)]
            return await asyncio.gather(*Tasks)

    async def SendOne(self, aRecSes: TRecSes) -> dict:
        async with aiohttp.ClientSession(auth=self._GetAuth()) as Session:
            return await self._SendTry(Session, aRecSes)


class TRequestJson(TRequest):
    async def _Send(self, aSession: aiohttp.ClientSession, aRecSes: TRecSes) -> dict:
        async with aSession.post(aRecSes.Url, json=aRecSes.DataSend) as Response:
            Data = await Response.json()
            return {'data': Data, 'status': Response.status}

    async def Send(self, aUrl: str, aData: dict) -> dict:
        RecSes = TRecSes(aUrl, aData)
        return await self.SendOne(RecSes)


class TRequestGet(TRequest):
    async def _Send(self, aSession: aiohttp.ClientSession, aRecSes: TRecSes) -> dict:
        async with aSession.get(aRecSes.Url) as Response:
            if (aRecSes.OnRead):
                Res = await aRecSes.OnRead(aRecSes, Response)
            else:
                Res = await Response.read()
            return {'data': Res, 'status': Response.status}

    async def Send(self, aUrl: str) -> dict:
        RecSes = TRecSes(aUrl)
        return await self.SendOne(RecSes)


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
