# Created: 2024.10.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
import aiohttp


def DictToCookie(aDict) -> str:
    return '; '.join([f'{Key}={Val}' for Key, Val in aDict.items()])

async def UrlGetData(aUrl: str, aLogin: str = None, aPassword: str = None, aHeaders: dict = None):
    Auth = None
    if (aLogin and aPassword):
        Auth = aiohttp.BasicAuth(login=aLogin, password=aPassword)

    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept-Language': 'uk'
    }

    if (aHeaders):
        for Key, Val in aHeaders.items():
            if isinstance(Val, dict):
                Val = DictToCookie(Val)
            Headers[Key] = Val

    TimeAt = time.time()
    try:
        async with aiohttp.ClientSession(auth=Auth, headers=Headers, max_field_size=16384) as Session:
            async with Session.get(aUrl, allow_redirects=True) as Response:
                if (Response.status == 200):
                    Data = await Response.read()
                    Res = {'status': Response.status, 'data': Data}
                else:
                    Res = {'status': Response.status}
    except Exception as E:
        Res = {'err': str(E), 'status': -1}

    Res['time'] = round(time.time() - TimeAt, 2)
    return Res
