# Created: 2024.04.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from Inc.DbList.DbUtil import TJsonEncoder
from Inc.Scheme.Scheme import TScheme
import IncP.LibCtrl as Lib
from .Util import GetSoup, UrlGetData


async def Parse(self, aData: dict) -> dict:
    Script = Lib.DeepGetByList(aData, ['post', 'script'])
    try:
        Script = json.loads(Script)
        Type = list(Script.keys())[0]
    except Exception as E:
        return {'err': f'json {E}'}

    Urls = Lib.DeepGetByList(Script, [Type, 'info', 'url'])
    if (Urls):
        if (not isinstance(Urls, list)):
            return {'err': f'not a list: {Type}->info->url'}
        Urls = [xUrl for xUrl in Urls if xUrl.startswith('http')]
        if (not Urls):
            return {'err': 'no urls with http prefix'}

        UrlData = await UrlGetData(Urls[0])
        if (UrlData['status'] != 200):
            return {'err': f'download status code {UrlData["status"]}'}
    else:
        UrlData = {
            'data': f'''
                <html>
                    <body>
                        No {Type}->info->url section found !
                        The quick brown fox jumps over the lazy dog.
                    </body>
                </html>
            '''
        }

    BSoup = GetSoup(UrlData['data'])
    Scheme = TScheme(Script)
    Scheme.Parse(BSoup)
    Pipe = Scheme.GetPipe(Type)

    PipeStr = json.dumps(Pipe, indent=2, ensure_ascii=False, cls=TJsonEncoder)
    return {
        'err': '\n'.join(Scheme.Err),
        'data': PipeStr
    }
