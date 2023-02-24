# Created: 2021.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
import json
#
from Inc.DbList import TDbListSafe
from Inc.Util.Obj import DeepGet
from Inc.Misc.Misc import FilterKey, FilterKeyErr
from Inc.WebSrv.WebApi import TApiBase, TWebClient
#from IncP.Download import TDownload, TDHeaders, GetSoup, GetSoupUrl
#from IncP.Scheme.Scheme import TScheme
#from IncP.Scheme.SchemeApi import TSchemeApi


class TApiPlugin():
    def __init__(self, aArgs: dict = None):
        if (aArgs is None):
            aArgs = {}

        self.Args = aArgs
        self.Res = []
        self.Hash = {}


class TApi(TApiBase):
    def __init__(self):
        super().__init__()

        self.Url = {
            'get_scheme_empty':         {'param': ['cnt']},
            'get_scheme_not_empty':     {'param': ['cnt']},
            'get_scheme_mederate':      {'param': []},
        }

        self.DefMethod = self.DefHandler
        self.WebClient = TWebClient()

        #self.PluginAdd(get_scheme_find, {'web_client': self.WebClient})

    async def _DoAuthRequest(self, aUser: str, aPassw: str):
        return True

    async def DefHandler(self, aPath: str, aData: dict = None) -> dict: #//
        if (aData is None):
            aData = {}
        return await self.WebClient.Send(f'web/{aPath}', aData)


Api = TApi()
