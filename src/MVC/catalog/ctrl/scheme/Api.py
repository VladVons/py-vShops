# Created: 2024.04.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
import IncP.LibCtrl as Lib
from Inc.Scheme.Scheme import TSoupScheme
from .Util import GetSoup, GetUrlData


async def Parse(self, aData: dict) -> dict:
    Script = Lib.DeepGetByList(aData, ['post', 'script'])
    try:
        Script = json.loads(Script)
    except Exception as E:
        return {'err': f'json {E}'}

    Url = Lib.DeepGetByList(Script, ['product', 'info', 'url'])
    if (not Url):
        return {'err': 'path not found: product->info->url'}

    if (not isinstance(Url, list)):
        return {'err': 'not a list: product->info->url'}

    UrlData = await GetUrlData(Url[0])
    if (UrlData['status'] != 200):
        return {'err': f'download status code {UrlData["status"]}'}

    Soup = GetSoup(UrlData['data'])
    SoupScheme = TSoupScheme()
    Res = SoupScheme.Parse(Soup, Script)

    Pipe = Lib.DeepGetByList(Res, ['product', 'pipe'])
    return {
        'err': '\n'.join(SoupScheme.Err),
        'data': json.dumps(Pipe, indent=2, ensure_ascii=False)
    }
