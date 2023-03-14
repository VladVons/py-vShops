# Created: 2022.10.19
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
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

def ParseUserAgent(aValue: str) -> dict:
    # Data  = [
    # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    # 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
    # 'Mozilla/5.0 (Linux; Android 10; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
    # 'Mozilla/5.0 (Linux; Android 12; M2102J20SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15',
    # 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
    # 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    # 'Wget/1.21.2',
    # 'curl/7.81.0'
    # ]

    OS = ''
    Browser = ''

    Pattern = r"\((.*?)\).*(chrome|firefox|safari|opr|gecko$)/*(.*)"
    try:
        UArr = re.findall(Pattern, aValue, re.IGNORECASE)
        if (UArr):
            OS = UArr[0][0].split(';')[1].strip()
            Browser = f'{UArr[0][1]}-{UArr[0][2]}'
        else:
            Browser = aValue
    except Exception:
        Browser = ''
    return {'os': OS.lower(), 'browser': Browser.lower()}
