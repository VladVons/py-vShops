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
    # 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/116.0.1938.76 Safari/537.36',
    # 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
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

    Browser = ''
    OS = ''
    try:
        Pattern = r"\((.*?)\).*(chrome|firefox|safari|opr|edge|opera|gecko$)/*(.*)"
        UArr = re.findall(Pattern, aValue, re.IGNORECASE)
        if (UArr):
            Browser = f'{UArr[0][1]}-{UArr[0][2]}'
            OS = UArr[0][0].split(';')[1].strip()
        else:
            Browser = aValue
    except Exception:
        pass
    return {'os': OS.lower(), 'browser': Browser.lower().replace("'", '"')}

def UrlDecode(aUrl: str) -> dict:
    Res = {}
    for xParam in aUrl.split('&'):
        if (xParam):
            KeyVal = xParam.split('=')
            if (len(KeyVal) == 2):
                Res[KeyVal[0]] = KeyVal[1]
            else:
                Res[KeyVal[0]] = None
    return Res

def UrlEncode(aQuery: dict) -> str:
    Arr = [f'{Key}={Val}'for Key, Val in aQuery.items()]
    return '&'.join(Arr)

def UrlUdate(aUrl: str, aData: dict) -> str:
    if ('?' in aUrl):
        Path, Query = aUrl.split('?')
    else:
        Path = ''
        Query = aUrl

    Res = {}
    for xQuery in Query.split('&'):
        Pair = xQuery.split('=')
        if (len(Pair) == 2):
            Key, Val = Pair
            Res[Key] = Val
    Res.update(aData)
    Res = Path + '?' + '&'.join([f'{Key}={Val}' for Key, Val in Res.items()])
    return Res


# # urllib.robotparser doesnt filter
class TRobots():
    def __init__(self):
        self.Disallow = []

    def Parse(self, aText: str):
        for Line in aText.splitlines():
            if ('Disallow' in Line):
                Rule = Line.split(':')[1].strip()
                Rule = re.escape(Rule).replace("\\*", ".*")
                self.Disallow.append(Rule)

    def CheckUrl(self, aUrl: str) -> bool:
        for Rule in self.Disallow:
            if (re.match(Rule, aUrl)):
                return False
        return True
