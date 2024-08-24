# Created: 2024.06.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import time
import asyncio
import aiohttp
#
from IncP.Log import Log
from . import TSemQuery


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
