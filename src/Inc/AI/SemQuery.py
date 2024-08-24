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
        Log.Print(1, 'i', f'Preparing {self.CntDown} tasks')

        Sem = asyncio.Semaphore(aMaxConn)
        async with aiohttp.ClientSession() as Session:
            Tasks = []
            for xQuery in aQuery:
                Task = asyncio.create_task(self._QuerySem(xQuery, Session, Sem))
                Tasks.append(Task)
            return await asyncio.gather(*Tasks)
