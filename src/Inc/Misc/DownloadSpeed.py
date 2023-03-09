# Created: 2022.04.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# Url = 'https://speed.hetzner.de/100MB.bin'
# Url = 'http://212.183.159.230/20MB.zip'
# asyncio.run(TDownloadSpeed(2).Test(Url))


from urllib.parse import urlparse
import asyncio
import io
import ssl
import time
import requests
#
from Inc.Http.HttpLib import ReadHead


class TDownload():
    def __init__(self):
        self.BlockSize = 2**16
        self.Sleep = 0.01

    def OnBlock(self, aLen: int, aSize: int):
        pass

    def Request(self, aHost: str, aPath: str) -> str:
        Arr = [
            'GET %s HTTP/1.1' % aPath,
            'Host: %s' % aHost,
            #'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0',
            #'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            #'Accept-Language: uk-UA,uk;q=0.8,en-US;q=0.5,en;q=0.3',
            #'Connection: keep-alive',
            #'Accept-Encoding: gzip, deflate, br',
            #'Upgrade-Insecure-Requests: 1',
            #'Sec-Fetch-Dest: document',
            #'Sec-Fetch-Mode: navigate',
            #'Sec-Fetch-Site: none',
            #'Sec-Fetch-User: ?1',
            '\r\n'
        ]
        return '\r\n'.join(Arr)

    async def Get(self, aUrl: str, aStreamOut) -> int:
        UrlInfo = urlparse(aUrl)
        Port = UrlInfo.port
        if (Port is None):
            if (UrlInfo.scheme == 'https'):
                Port = 443
                SslCtx = ssl.create_default_context()
            else:
                Port = 80
                SslCtx = None
        Reader, Writer = await asyncio.open_connection(UrlInfo.hostname, Port, ssl=SslCtx)
        Data = self.Request(UrlInfo.hostname, UrlInfo.path).encode()
        Writer.write(Data)
        await Writer.drain()

        Res = 0
        Head = await ReadHead(Reader, False)
        if (Head.get('code') == '200'):
            Len = int(Head.get('content-length', '0'))
            if (Len > 0):
                while (True):
                    Data = await Reader.read(self.BlockSize)
                    if (not Data):
                        break

                    Res += len(Data)
                    if (self.OnBlock(Len, Res)):
                        break

                    aStreamOut.write(Data)
                    await asyncio.sleep(self.Sleep)
                aStreamOut.flush()
        Writer.close()
        return Res

    async def GetSync(self, aUrl: str, aStreamOut) -> int:
        Reader = requests.get(aUrl, stream=True, timeout=3)
        Res = 0
        Len = int(Reader.headers.get('content-length', '0'))
        if (Len > 0):
            for Data in Reader.iter_content(self.BlockSize):
                Res += len(Data)
                if (self.OnBlock(Len, Res)):
                    break

                aStreamOut.write(Data)
                await asyncio.sleep(self.Sleep)
        return Res


class TDownloadSpeed(TDownload):
    def __init__(self, aMaxDuration = 60):
        super().__init__()
        self.MaxDuration = aMaxDuration
        self.StartAt = None

    def OnBlock(self, aLen: int, aSize: int):
        Duration = time.time() - self.StartAt
        Unit = 10**6
        Msg = '%.2fM/%.2fM, %.2fMb' % (round(aSize / Unit, 2), round(aLen / Unit, 2), round(aSize / Duration / Unit * 8, 2))
        print('\r' + Msg, end='')
        return (Duration >= self.MaxDuration)

    async def Test(self, aUrl: str):
        self.StartAt = time.time()
        #with open('File.dat', 'wb') as IO:
        with io.BytesIO() as IO:
            Size = await self.Get(aUrl, IO)
            #Size = await self.GetSync(aUrl, IO)
        Duration = time.time() - self.StartAt
        return round(Size / Duration / 10**6 * 8, 2)
