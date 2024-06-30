# Created: 2024.06.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import time
import asyncio
import aiohttp
#
from IncP.Log import Log


class TSemQuery():
    CntDown = 0

    async def _Query(self, aMsg: str, aSession) -> str:
        raise NotImplementedError()

    async def _QuerySem(self, aMsg: str, aSession, aSem):
        async with aSem:
            Res = await self._Query(aMsg, aSession)
            self.CntDown -= 1
            Log.Print(1, 'i', f'Remains tasks: {self.CntDown}')
            return Res

    async def Exec(self, aQuery: list, aMaxConn: int):
        self.CntDown = len(aQuery)

        Sem = asyncio.Semaphore(aMaxConn)
        async with aiohttp.ClientSession() as Session:
            Tasks = []
            for xQuery in aQuery:
                Task = asyncio.create_task(self._QuerySem(xQuery, Session, Sem))
                Tasks.append(Task)
            return await asyncio.gather(*Tasks)


class TOpenAI(TSemQuery):
    def __init__(self):
        self.Url = 'https://api.openai.com/v1/chat/completions'
        self.Model = ['gpt-3.5-turbo', 'gpt-4-turbo']

        EnvKey = 'OPENAI_API_KEY'
        self.ApiKey = os.getenv(EnvKey)
        assert(self.ApiKey), f'Cant read environment variable `{EnvKey}`'

    async def _Query(self, aMsg: str, aSession) -> str:
        Headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.ApiKey}'
        }

        Data = {
            'model': self.Model[1],
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': aMsg}
            ]
        }

        async with aSession.post(self.Url, json=Data, headers=Headers) as Response:
            if (Response.status == 200):
                TimeAt = time.time()
                try:
                    Data = await Response.json()
                    Res = {'data': Data['choices'][0]['message']['content'], 'time': round(time.time() - TimeAt, 2)}
                except Exception as E:
                    Log.Print(1, 'x', f'_Query(). {self.Url}', aE = E)
                    Res = {'err': str(E)}
            else:
                Res = {'err': f'{Response.status}, {Response.text}, {Response.reason}'}
            return Res
