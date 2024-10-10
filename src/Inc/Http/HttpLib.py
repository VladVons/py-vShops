# Created: 2020.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio

async def ReadHead(aReader: asyncio.StreamReader, aServ = True) -> dict:
    Res = {}
    while True:
        Data = await aReader.readline()
        if (Data == b'\r\n') or (not Data):
            break

        Data = Data.decode('utf-8').strip()
        if (len(Res) == 0):
            if (aServ):
                Res['mode'], Res['url'], Res['prot'] = Data.split(' ')
                Res['path'], *Res['query'] = Res['url'].split('?')
            else:
                Res['prot'], Res['code'], *Res['status'] = Data.split(' ')
        else:
            Key, Value = Data.split(':', maxsplit=1)
            Res[Key.lower()] = Value.strip()
    return Res

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
                await asyncio.sleep(0.01)
            aStream.flush()
    await Writer.wait_closed()
