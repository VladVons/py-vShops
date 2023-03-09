# Created: 2021.01.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


try:
    import asyncio
except ModuleNotFoundError:
    import uasyncio as asyncio

#
from .HttpLib import ReadHead


async def UrlLoad(aUrl: str, aStream):
    _, _, Host, Path = aUrl.split('/', 3)
    Reader, Writer = await asyncio.open_connection(Host, 80)
    Data = bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (Path, Host), 'utf8')
    await Writer.awrite(Data)
    await Writer.drain()

    Head = await ReadHead(Reader, False)
    if (Head.get('code', '404') == '200'):
        Len = int(Head.get('content-length', 0))
        if (Len > 0):
            while True:
                Data = await Reader.read(512)
                if (not Data):
                    break
                aStream.write(Data)
                await asyncio.sleep_ms(10)
            aStream.flush()
    await Writer.wait_closed()

def UrlPercent(aData: bytearray) -> str:
    Bits = aData.split(b'%')
    Arr = [Bits[0]]
    for Item in Bits[1:]:
        Code = Item[:2]
        Char = bytes([int(Code, 16)])
        Arr.append(Char)
        Arr.append(Item[2:].replace(b'+', b' '))
    Res = b''.join(Arr)
    return Res.decode('utf-8')
