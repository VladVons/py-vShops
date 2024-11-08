# Created: 2024.10.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
import asyncio
import aiohttp
import ssl

def DictToCookie(aDict) -> str:
    return '; '.join([f'{Key}={Val}' for Key, Val in aDict.items()])

def UrlGetDataSync(aUrl: str, aHeaders: dict = None) -> dict:
    import requests # slow
    Response = requests.get(aUrl, timeout=3, headers=aHeaders)
    if (Response.status_code == 200):
        Res = {'status': Response.status_code, 'data': Response.content}
    else:
        Res = {'status': Response.status_code}
    return Res

async def UrlGetData(aUrl: str, aLogin: str = None, aPassword: str = None, aHeaders: dict = None):
    # todo. cant read url with %2C
    # https://mrpecet.pl/pl/p/Apple-MacBook-Pro-15-2015-i7-2%2C5GHz-16GB-512GB-AMD-R9-M370X/576

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

    # solved. unable to get local issuer certificate. problem loading https://hardwaredirect.pl
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    TimeAt = time.time()
    try:
        async with aiohttp.ClientSession(auth=Auth, headers=Headers, max_field_size=16384) as Session:
            async with Session.get(aUrl, allow_redirects=True, ssl=ssl_context) as Response:
                if (Response.status == 200):
                    Data = await Response.read()
                    Res = {'status': Response.status, 'data': Data}
                else:
                    # todo https://nosta.com.ua
                    await asyncio.sleep(1)
                    TimeAt = time.time()
                    Res = UrlGetDataSync(aUrl, Headers)
    except Exception as E:
        EType = type(E).__name__
        Res = {'err': f'{EType}, {E}' , 'status': -1}

    Res['time'] = round(time.time() - TimeAt, 2)
    return Res
