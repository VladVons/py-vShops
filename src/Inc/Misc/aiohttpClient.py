# Created: 2024.10.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import time
import asyncio
import aiohttp
import ssl


def DictToCookie(aDict) -> str:
    return '; '.join([f'{Key}={Val}' for Key, Val in aDict.items()])

def UrlGetDataSync(aUrl: str, aHeaders: dict = None, aStatusOnly = False) -> dict:
    import requests # slow load

    Response = requests.get(aUrl, timeout=3, headers=aHeaders, allow_redirects = True)
    if (aStatusOnly):
        Res = {'status': Response.status_code, 'data': None}
    else:
        if (Response.status_code == 200):
            Res = {'status': Response.status_code, 'data': Response.content}
        else:
            Res = {'status': Response.status_code}
    return Res

async def UrlGetData(aUrl: str, aLogin: str = None, aPassword: str = None, aHeaders: dict = None, aStatusOnly: bool = False, aProxy: dict = None):
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

    ProxyUrl = ProxyAuth = None
    if (aProxy):
        ProxyUrl = f"{aProxy['scheme']}://{aProxy['host']}:{aProxy['port']}"
        Login = aProxy.get('login')
        if (Login):
            ProxyAuth = aiohttp.BasicAuth(Login, aProxy.get('passw'))

    # solved. unable to get local issuer certificate. problem loading https://hardwaredirect.pl
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE


    TimeAt = time.time()
    if ('%' in aUrl):
        # https://mrpecet.pl/pl/p/Apple-MacBook-Pro-15-2015-i7-2%2C5GHz-16GB-512GB-AMD-R9-M370X/576
        # todo. aiohttp.ClientSession err: too many redirects when url has '%XX'
        Res = UrlGetDataSync(aUrl, Headers)
    else:
        try:
            async with aiohttp.ClientSession(auth=Auth, headers=Headers, max_field_size=16384) as Session:
                async with Session.get(aUrl, allow_redirects=True, ssl=ssl_context, proxy=ProxyUrl, proxy_auth=ProxyAuth) as Response:
                    if (Response.status == 200):
                        if (aStatusOnly):
                            Data = None
                        else:
                            Data = await Response.read()
                        Res = {'status': Response.status, 'data': Data}
                    else:
                        # todo https://nosta.com.ua
                        await asyncio.sleep(1)
                        TimeAt = time.time()
                        Res = UrlGetDataSync(aUrl, Headers, aStatusOnly=aStatusOnly)
        except Exception as E:
            EType = type(E).__name__
            Res = {'err': f'{EType}, {E}' , 'status': -1}

    Res['time'] = round(time.time() - TimeAt, 2)
    return Res

async def DownloadChunks(aUrl: str, aBlockSize: int) -> iter:
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    SSL = ssl.create_default_context()
    #SSL.check_hostname = False
    #SSL.verify_mode = ssl.CERT_NONE
    #SSL.options |= ssl.OP_NO_TLSv1_2
    SSL.options = 0

    async with aiohttp.ClientSession(headers=Headers) as Session:
        async with Session.get(aUrl, ssl=SSL) as Response:
            if (Response.status == 200):
                TotalSize = int(Response.headers.get('Content-Length', 0))
                async for xBlock in Response.content.iter_chunked(aBlockSize):
                    yield (xBlock, TotalSize)

async def DownloadChunksToFile(aUrl: str, aFile: str, aBlockSize: int = 65536):
    if (os.path.exists(aFile)):
        os.remove(aFile)

    Size = 0
    async for xBlock, xTotalSize in DownloadChunks(aUrl, aBlockSize):
        with open(aFile, 'ab') as F:
            F.write(xBlock)

            Size += len(xBlock)
            print(f'\rDownload: {Size / xTotalSize * 100:.1f}%', end='')
