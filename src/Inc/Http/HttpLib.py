# Created: 2020.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
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


def UrlParse(aUrl: str) -> dict:
    # by cx 2023.03.20
    Pattern = r'^([^:]+)://([^:?#/]+)[:]?(\d*)([/]?[^?#]*)[?]?([^#]*)[#]?(.*)'
    Parts = re.findall(Pattern, aUrl, flags=re.ASCII)
    Keys = ('scheme', 'host', 'port', 'path', 'query', 'hash')
    return dict(zip(Keys, Parts[0]))

def UrlParseValidate(aUrl: str) -> list:
    # by cx 2023.03.20
    Pattern = r'^([a-z]{2,})://([a-z0-9]{1}[a-z0-9-.]*[a-z0-9]{1})[:]?(\d*)([/]?[a-zA-Z0-9-_.%]*)[?]?([a-zA-Z0-9-_.%=&]*)[#]?(.*)'
    return re.findall(Pattern, aUrl, flags=re.ASCII)
