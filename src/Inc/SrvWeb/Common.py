# Created: 2022.10.19
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
from aiohttp import streamer


MaxLen = 2 ** 16


@streamer
async def FileReader(writer, aFile: str) -> int:
    Res = 0
    with open(aFile, 'rb') as File:
        Buf = File.read(MaxLen)
        Res += len(Buf)
        while (Buf):
            await writer.write(Buf)
            Buf = File.read(MaxLen)
            Res += len(Buf)
            await asyncio.sleep(0.01)
    return Res

async def FileWriter(aReader, aFile: str) -> int:
    Res = 0
    with open(aFile, 'wb') as File:
        Buf = aReader.read(MaxLen)
        Res += len(Buf)
        while (Buf):
            File.write(Buf)
            Buf = aReader.read(MaxLen)
            Res += len(Buf)
            await asyncio.sleep(0.01)
    return Res
