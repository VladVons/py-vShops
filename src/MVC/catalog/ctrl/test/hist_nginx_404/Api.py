# Created: 2024.06.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re
import IncP.LibCtrl as Lib


async def NginxFilterBotErr404(aFiles: list[str]) -> Lib.TDbList:
    Res = Lib.TDbList(['ip', 'path'])
    Pattern = re.compile(r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>[A-Z]+) (?P<path>[^ ]+) (?P<protocol>[^"]+)" (?P<status>\d+) (?P<size>\d+) "(?P<referrer>[^"]*)" "(?P<agent>[^"]*)"')
    for xFile in aFiles:
        if (os.path.exists(xFile)):
            with open(xFile, 'r', encoding='utf8') as F:
                for xLine in F.readlines():
                    if ('bot' in xLine):
                        Match = Pattern.match(xLine)
                        if (Match):
                            Data = Match.groupdict()
                            if (Data.get('status') == '404'):
                                Row = [Data.get('ip'), Data.get('path')]
                                Res.RecAdd(Row)
    return Res

async def Main(self, aData: dict = None) -> dict:
    Res = await NginxFilterBotErr404(
        ['/var/log/nginx/1x1.com.ua.log_access.log',
         '/var/log/nginx/1x1.com.ua.log_access.log.1'
        ])

    return {'dbl': Res.Export()}
