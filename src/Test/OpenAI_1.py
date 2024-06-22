# ChatGPT async example
# 2023.12.08, VladVons@gmail.com

import os
import time
import asyncio
import aiohttp


class TOpenAI():
    def __init__(self):
        self.Url = 'https://api.openai.com/v1/chat/completions'

        EnvKey = 'OPENAI_API_KEY'
        self.ApiKey = os.getenv(EnvKey)
        assert(self.ApiKey), f'Cant read environment variable `{EnvKey}`'

        self.CntDown = 0

    async def Query(self, aMsg: str, aSession) -> str:
        Headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.ApiKey}'
        }

        Data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': aMsg}
            ]
        }

        async with aSession.post(self.Url, json=Data, headers=Headers) as Response:
            if (Response.status == 200):
                Data = await Response.json()
                Res = Data['choices'][0]['message']['content']
            else:
                Res = f'Err: {Response.status}, {Response.text}'

            self.CntDown -= 1
            print(f'Remains tasks: {self.CntDown}')
            return Res

    async def QuerySem(self, aMsg: str, aSession, aSem):
        async with aSem:
            return await self.Query(aMsg, aSession)

    async def Main(self, aQuery: list, aMaxConn: int):
        self.CntDown = len(aQuery)

        Sem = asyncio.Semaphore(aMaxConn)
        async with aiohttp.ClientSession() as Session:
            Tasks = []
            for xQuery in aQuery:
                Task = asyncio.create_task(self.QuerySem(xQuery, Session, Sem))
                Tasks.append(Task)
            Res = await asyncio.gather(*Tasks)

            for Idx, (xQuery, xRes) in enumerate(zip(aQuery, Res)):
                print(f'запитання {Idx + 1}: {xQuery}')
                print(f'відповідь: {xRes}')
                print()

Queries = [
    'обчисли 2+3*4',
    'скільки людей на планеті ?',
    'яка столиця Росії ?',
    'скідьки сантиметрів має дюйм ?',
    'яка відстань від Землі до сонця ?',
    'яке прискорення вільного падіння тіла на Землі, Місяці, Сонці ?',
    'яка найвища точка в Україні ?',
    'скільки важить літр спирту 96% ?'
]

StartAt = time.time()
asyncio.run(TOpenAI().Main(Queries, 5))
Elapsed = time.time() - StartAt
print(f'час: {Elapsed :.2f}, середнє: {Elapsed/len(Queries) :.2f}')
