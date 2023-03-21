# Created: 2023.03.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# async with TClientSession(aHost = 'https://httpbin.org') as Session:
#     Data = await Session.Json('/post', {'method': 'help'})
#
# async with TDownloadSpeed(aHost = 'https://speed.hetzner.de') as Session:
#     await Session.Test('/1GB.bin')
#
# echo test
# https://httpbin.org/get
# https://httpbin.org/post
# curl -X POST "https://httpbin.org/post" -H "Content-Type: application/json" -d '{"city": "ternopil"}'



import io
import ssl
import time
import json
import asyncio
#
from Inc.Http.HttpLib import ReadHead, UrlParse
from Inc.DataClass import DDataClass


@DDataClass
class TResponce():
    Status: int
    Size: int
    Time: float
    Head: dict
    Data: str = None


class TClientSession():
    def __init__(self, aHost: str = None):
        self.Host: str
        self.Port: int
        self.Ssl: object
        self.Reader: asyncio.StreamReader = None
        self.Writer: asyncio.StreamWriter = None

        self.Timeout = 5
        self.BlockSize = 2**16

        Url = self._Init(aHost)
        Path = Url['path']
        if (Path):
            raise ValueError(f'Path must be absolute rooted {Path}')
        self.Host = Url['host']

    async def __aenter__(self) -> 'TClientSession':
        await self.Connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.Close()

    def _CreateRequest(self, aData: dict) -> str:
        Res = [f'{Key}:{Val}' for Key, Val in aData.items() if not Key.startswith('_')]
        Res.append('\r\n')
        Res.insert(0, f'{aData["_mode"]} {aData["_path"]} HTTP/1.1')
        return '\r\n'.join(Res)

    def _DoProgress(self, aSize: int, aOffset: int):
        pass

    def _Init(self, aUrl: str) -> dict:
        Url = UrlParse(aUrl)
        Scheme = Url['scheme']
        Port = int(Url['port'] or '0')
        if (Scheme == 'https'):
            self.Port = Port if Port else 443
            self.Ssl = ssl.create_default_context()
        elif (Scheme == 'http'):
            self.Port = Port if Port else 80
            self.Ssl = None
        else:
            raise ValueError(f'Invalid scheme {Scheme}')
        return Url

    async def _LoadChains(self, aWriter: io.RawIOBase) -> int:
        Res = 0
        while (True):
            Data = await self.Reader.readline()
            Len = int(Data.decode('utf-8'), 16)
            if (Len == 0):
                break

            await self._LoadLen(aWriter, Len)
            await self.Reader.readline()
            Res += Len

            self._DoProgress(0, Res)
        return Res

    async def _LoadLen(self, aWriter: io.RawIOBase, aLen: int) -> int:
        Res = 0
        while (Res < aLen):
            Len = min(self.BlockSize, aLen - Res)
            Data = await self.Reader.read(Len)
            aWriter.write(Data)
            Res += len(Data)

            self._DoProgress(aLen, Res)
        return Res

    async def _LoadLines(self, aWriter: io.RawIOBase) -> int:
        Res = 0
        while (True):
            Data = await self.Reader.readline()
            if (Data == b''):
                break

            aWriter.write(Data)
            Res += len(Data)
        return Res

    async def _LoadToStream(self, aWriter: io.RawIOBase, aPath: str, aMode: str = 'GET', aData: dict = None) -> TResponce:
        StartAt = time.time()

        Param = {'_path': aPath, '_mode': aMode, 'host': self.Host}
        if (aData):
            Param.update(aData)

        Data = self._CreateRequest(Param).encode()
        self.Writer.write(Data)
        if ('_data' in aData):
            self.Writer.write(aData['_data'])
        await self.Writer.drain()

        Head = await ReadHead(self.Reader, False)
        Len = int(Head.get('content-length', '0'))
        if (Len == 0):
            if (Head.get('transfer-encoding') == 'chunked'):
                Size = await self._LoadChains(aWriter)
            else:
                Size = await self._LoadLines(aWriter)
        else:
            Size = await self._LoadLen(aWriter, Len)
        aWriter.flush()

        return TResponce(
            Status = int(Head.get('code')),
            Size = Size,
            Time = time.time() - StartAt,
            Head = Head
        )

    async def Connect(self):
        Task = asyncio.open_connection(self.Host, self.Port, ssl = self.Ssl)
        # ToDo. 3x slower
        self.Reader, self.Writer = await asyncio.wait_for(Task, timeout = self.Timeout)

    async def Close(self):
        if (self.Writer):
            self.Writer.close()
            await self.Writer.wait_closed()
            self.Writer = None
            self.Reader = None

    async def Download(self, aPath: str, aFile: str = None) -> TResponce:
        if (not aFile):
            aFile = aPath.rsplit('/', maxsplit=1)[-1]

        with open(aFile, 'wb') as F:
            return await self._LoadToStream(F, aPath)

    async def Get(self, aPath: str) -> TResponce:
        with io.BytesIO() as IO:
            Res = await self._LoadToStream(IO, aPath)
            Res.Data = IO.getvalue().decode()
            return Res

    async def Post(self, aPath: str, aData: str = None) -> TResponce:
        with io.BytesIO() as IO:
            Param = {}
            if (aData):
                Data = aData.encode()
                Param['content-length'] = len(Data)
                Param['_data'] = Data
            Res = await self._LoadToStream(IO, aPath, 'POST', Param)
            Res.Data = IO.getvalue().decode()
            return Res

    async def Json(self, aPath: str, aData: dict = None) -> TResponce:
        with io.BytesIO() as IO:
            Param = {'content-type': 'application/json'}
            if (aData):
                Data = json.dumps(aData).encode()
                Param['content-length'] = len(Data)
                Param['_data'] = Data
            Res = await self._LoadToStream(IO, aPath, 'POST', Param)
            if (Res.Status == 200):
                Res.Data = json.loads(IO.getvalue().decode())
            return Res


class TDownloadSpeed(TClientSession):
    class TFakeIO(io.IOBase):
        def flush(self): ...
        async def write(self, _aData): ...

    def __init__(self, aHost: str, aMaxDuration = 60):
        super().__init__(aHost)
        self.MaxDuration = aMaxDuration
        self.StartAt = time.time()

    def _DoProgress(self, aSize: int, aOffset: int):
        Duration = time.time() - self.StartAt
        Unit = 10**6
        Msg = f'{aSize / Unit :5.2f}M/{aOffset / Unit :5.2f}M, {aSize / Duration / Unit * 8 :5.2f}Mb'
        print('\r' + Msg, end='')
        return (Duration >= self.MaxDuration)

    async def Test(self, aPath: str) -> float:
        self.StartAt = time.time()
        Res = await self._LoadToStream(TDownloadSpeed.TFakeIO(), aPath)
        Duration = time.time() - self.StartAt
        return round(Res.Size / Duration / 10**6 * 8, 2)
