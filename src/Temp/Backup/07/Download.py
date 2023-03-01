# Created: 2022.10.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
import json
import asyncio
import aiohttp
#
from IncP.Log import Log


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

    def Get(self) -> aiohttp.BasicAuth:
        return aiohttp.BasicAuth(login=self.User, password=self.Passw)


class TCheckUrls():
    def __init__(self):
        self._Count = 0

    async def _OnSend(self, aRecSes: TRecSes, aResponse: aiohttp.ClientResponse):
        if (aRecSes.TaskNo % 100 == 0):
            print(f'Check {aRecSes.TaskNo:4}/{self._Count}, {aRecSes.Url}')
        #while await aResponse.content.readany()
        return (aResponse.status == 200)

    async def Run(self, aUrls: list, aTasks: int = 5, aSleep: int = 0):
        self._Count = len(aUrls)
        Download = TDownload()
        Download.Sleep = aSleep
        RecSes = [TRecSes(x, aOnRead=self._OnSend) for x in aUrls]
        Res = await Download.SendMany(RecSes, aTasks)
        return Res


class TRequest():
    def __init__(self, aCallBack = None):
        self.CallBack: callable = aCallBack
        self.Auth = None
        self.Sleep = 0

    async def _SendSem(self, aSession: aiohttp.ClientSession, aSem: asyncio.Semaphore, aRecSes: TRecSes, aTaskNo: int = 0) -> dict:
        async with aSem:
            aRecSes.TaskNo = aTaskNo
            return await self._Send(aSession, aRecSes)

    async def Send(self, aSession: aiohttp.ClientSession, aRecSes: TRecSes) -> dict:
        await asyncio.sleep(self.Sleep)
        TimeAt = time.time()
        try:
            if (aRecSes.DataSend is None):
                async with aSession.get(aRecSes.Url) as Response:
                    if (aRecSes.OnRead):
                        return await aRecSes.OnRead(aRecSes, Response)
                    Data = await Response.read()
            else:
                Type = type(aRecSes.DataSend)
                if (Type in [dict, list]):
                    async with aSession.post(aRecSes.Url, json=aRecSes.DataSend) as Response:
                        Data = await Response.json()
                else:
                    async with aSession.post(aRecSes.Url, data=aRecSes.DataSend) as Response:
                        Data = await Response.read()

            if (Response.content_type == 'application/json'):
                Data = json.loads(Data)
            Res = {'data': Data, 'status': Response.status, 'time': round(time.time() - TimeAt, 2)}
        except (aiohttp.ClientConnectorError, aiohttp.ClientError, aiohttp.InvalidURL, asyncio.TimeoutError) as E:
            Log.Print(1, 'e', 'Url %s, %s' % (aRecSes.Url, E))
            Res = {'data': E, 'status': -1, 'time': round(time.time() - TimeAt, 2)}

        if (self.CallBack):
            Res = await self.CallBack(aRecSes, Res)
        return Res

    async def SendMany(self, aTRecSes: list, aMaxTask: int = 5) -> list:
        Sem = asyncio.Semaphore(aMaxTask)
        async with aiohttp.ClientSession(auth=self.Auth) as Session:
            Tasks = [asyncio.create_task(self._SendSem(Session, Sem, RecSes, Idx)) for Idx, RecSes in enumerate(aTRecSes)]
            return await asyncio.gather(*Tasks)

    async def SendOne(self, aRecSes: TRecSes) -> dict:
        async with aiohttp.ClientSession(auth=self.Auth) as Session:
            return await self._Send(Session, aRecSes)

class TRequestJson(TRequest):

