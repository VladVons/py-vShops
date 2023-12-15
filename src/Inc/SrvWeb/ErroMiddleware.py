# Created: 2022.10.19
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import traceback
from aiohttp import web
#
from IncP.Log import Log


def CreateErroMiddleware(aOverrides: dict):
    @web.middleware
    async def ErroMiddleware(request: web.Request, handler):
        try:
            return await handler(request)
        except web.HTTPException as E:
            Override = aOverrides.get(E.status)
            if (Override):
                return await Override(request)
            raise E
        except Exception as E:
            Log.Print(1, 'x', 'ErroMiddleware()', aE = E)

            Override = aOverrides.get('err_all')
            if (Override):
                cwd = os.getcwd() + '/'
                Data = traceback.format_exception(*sys.exc_info())
                Data = [x.replace(cwd, '').rstrip('^\n ') for x in Data]
                return await Override(request, Data)
            raise E
    return ErroMiddleware
