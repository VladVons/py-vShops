# Created: 2022.06.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
from aiohttp import web
import aiohttp_session
#
from Inc.DbList import TDbListSafe
from Inc.Util.Obj import DeepGet
from .Api import Api


class TSession():
    def __init__(self):
        self.Cnt = 0
        self.Data = {}

    async def Update(self, aRequest: web.Request): #//
        self.Data = await aiohttp_session.get_session(aRequest)
        if (self.Cnt % 5 == 0):
            await self.UpdateUserConfig()
        self.Cnt += 1

    @staticmethod
    def _CheckUserAccess(aUrl: str, aUrls: list[str]) -> bool: #//
        if (aUrls):
            for x in aUrls:
                if (x.strip()) and (not x.startswith('-')) and (re.match(x, aUrl)):
                    return True
        return False

    def CheckUserAccess(self, aUrl: str) -> bool: #//
        Grant = ['/$', '/form/login', '/form/about']
        Allow = DeepGet(self.Data, 'user_conf.interface_allow', '').split() + Grant
        Deny = DeepGet(self.Data, 'user_conf.interface_deny', '').split()
        return (self._CheckUserAccess(aUrl, Allow)) and (not self._CheckUserAccess(aUrl, Deny))

    async def UpdateUserConfig(self): #//
        UserId = self.Data.get('UserId')
        if (UserId):
            DataApi = await Api.DefHandler('get_user_config', {'id': UserId})
            DblJ = DeepGet(DataApi, 'data.data')
            if (DblJ):
                Conf = TDbListSafe().Import(DblJ).ExportPair('name', 'data')
                self.Data['user_conf'] = Conf

Session = TSession()
