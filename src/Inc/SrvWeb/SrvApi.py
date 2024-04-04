# Created: 2021.02.28
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import base64
import json
import time
import aiohttp
from aiohttp import web
#
from Inc.DbList import TDbList
from Inc.Util.Obj import DeepGet
from IncP.Log import Log


class TApiBase():
    def __init__(self):
        self.Url = {}
        self.DefMethod = None
        self.Plugin = {}

    async def _DoAuthRequest(self, aUser: str, aPassw: str) -> bool:
        raise NotImplementedError()

    @staticmethod
    def GetMethodName(aPath: str) -> str:
        return 'path_' + aPath.replace('/', '_')

    @staticmethod
    def CheckParam(aParam: dict, aPattern: list):
        Diff = set(aPattern) - set(aParam)
        if (Diff):
            return 'param not set. %s' % Diff

        Diff = set(aParam) - set(aPattern)
        if (Diff):
            return 'param unknown. %s' % Diff

    def PluginAdd(self, aCls: object, aArgs: dict = None) -> object:
        if (aArgs is None):
            aArgs = {}

        Name = aCls.__name__
        if (not self.Url.get(Name)):
            Res = aCls(aArgs)
            self.Url[Name] = aCls.Param
            self.Url[Name]['class'] = Res
            return Res

    async def Call(self, aPath: str, aParam: dict) -> dict:
        UrlInf = self.Url.get(aPath)
        if (not UrlInf):
            return {'type': 'err', 'data': 'unknown url %s' % (aPath)}

        MethodName = self.GetMethodName(aPath)
        Method = getattr(self, MethodName, None)
        if (not Method):
            Class = UrlInf.get('class')
            if (Class):
                Method = getattr(Class, 'Exec', self.DefMethod)
            else:
                Method = self.DefMethod

            if (not Method):
                return {'type': 'err', 'data': 'unknown method %s' % (aPath)}

        ParamInf = UrlInf.get('param')
        if (ParamInf) and (ParamInf[0] == '*'):
            ParamInf = aParam.keys()

        ErrMsg = self.CheckParam(aParam, ParamInf)
        if (ErrMsg):
            Log.Print(1, 'e', ErrMsg)
            Res = {'type': 'err', 'data': ErrMsg}
        else:
            try:
                Data = await Method(aPath, aParam)
            except Exception as E:
                Data = None
                Log.Print(1, 'x', 'Call()', aE = E)
            Res = {'data': Data}
        return Res

    async def AuthRequest(self, aRequest: web.Request, aAuth: bool = True) -> bool:
        if (aAuth):
            Auth = aRequest.headers.get('Authorization')
            if (Auth):
                User, Passw = base64.b64decode(Auth.split()[1]).decode().split(':')
                return await self._DoAuthRequest(User, Passw)
        else:
            return True



class TWebClient():
    def __init__(self, aAuth: dict = None):
        self.Auth = aAuth or {}

    async def Send(self, aPath: str, aPost: dict = None):
        if (aPost is None):
            aPost = {}

        Auth = aiohttp.BasicAuth(self.Auth.get('user'), self.Auth.get('password'))
        Url = 'http://%s:%s/%s' % (self.Auth.get('server'), self.Auth.get('port'), aPath)
        TimeAt = time.time()
        try:
            async with aiohttp.ClientSession(auth=Auth) as Session:
                async with Session.post(Url, json=aPost) as Response:
                    Data = await Response.json()
                    Res = {'data': Data, 'status': Response.status, 'time': round(time.time() - TimeAt, 2)}
        except (aiohttp.ContentTypeError, aiohttp.ClientConnectorError, aiohttp.InvalidURL) as E:
            Log.Print(1, 'x', 'Send(). %s' % (Url), aE = E)
            Res = {'type': 'err', 'data': E, 'msg': Url, 'time': round(time.time() - TimeAt, 2)}
        return Res


class TWebSockClient():
    def __init__(self, aAuth: dict = None):
        if (aAuth is None):
            aAuth = {}

        self.Auth = aAuth
        self.OnMessage = None
        self.WS = None

    async def Connect(self, aPath: str, aParam: dict = None):
        if (aParam is None):
            aParam = {}

        Auth = aiohttp.BasicAuth(self.Auth.get('user'), self.Auth.get('password'))
        Url = 'http://%s:%s/%s' % (self.Auth.get('server'), self.Auth.get('port'), aPath)
        async with aiohttp.ClientSession(auth=Auth) as Session:
            async with Session.ws_connect(Url, params=aParam) as self.WS:
                async for Msg in self.WS:
                    if (Msg.type == aiohttp.WSMsgType.TEXT):
                        Data = json.loads(Msg.data)
                        await self.DoMessage(Data)
                    elif (Msg.type in [aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR]):
                        break

    async def Close(self):
        if (self.WS):
            await self.WS.close()

    async def Send(self, aData: dict):
        await self.WS.send_json(aData)

    async def DoMessage(self, aData):
        if (self.OnMessage):
            await self.OnMessage(aData)


class TWebSockSrv():
    def __init__(self):
        self.DblWS = TDbList(['ws', 'id'])
        self.Api = None

    async def Handle(self, aRequest: web.Request) -> web.WebSocketResponse:
        WS = web.WebSocketResponse()
        await WS.prepare(aRequest)
        try:
            #Id = aRequest.headers.get('Sec-WebSocket-Key')
            Id = aRequest.query.get('id')
            self.DblWS.RecAdd([WS, Id])
            async for Msg in WS:
                if (Msg.type == web.WSMsgType.text):
                    Plugin = aRequest.query.get('plugin')
                    if (Plugin):
                        Class = DeepGet(self.Api.Url, Plugin + '.Class')
                        if (Class is None):
                            await WS.send_json({'type': 'err', 'data': 'Unknown plugin %s' % (Plugin)})
                        else:
                            Data = Msg.json()
                            Param = Data.get('param', {})
                            Param['ws'] = (self.DblWS, Param.get('ws'))
                            await Class.Exec(Plugin, Param)
        except Exception as E:
            Log.Print(1, 'x', 'AddHandler()', aE=E)
        finally:
            self.DblWS.RecNo = 0
            RecNo = self.DblWS.FindField('ws', WS)
            self.DblWS.RecPop(RecNo)
        return WS
