# Created: 2022.10.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
import asyncio
import aiohttp


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
        self.Session.close()

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
