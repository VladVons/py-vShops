# Created: 2023.03.03
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
import time
from wtforms import Form
from aiohttp import web
from aiohttp_session import Session, get_session
#
from Inc.DbList import TDbList
from Inc.DictDef import TDictDef
from Inc.Loader.Api import TLoaderApi
from Inc.Misc.Jinja import TTemplate
from Inc.SrvWeb.Common import ParseUserAgent
from IncP import GetAppVer


class TFormBase(Form):
    '''
        Base class for rendering string from templates
    '''

    def __init__(self, aParent, aRequest: web.Request):
        super().__init__()

        self.Parent = aParent
        self.Ctrl: TLoaderApi = aParent.Loader['ctrl']
        self.Request = aRequest
        self.Tpl: TTemplate = aParent.Tpl
        self.Session: Session = None

        self.out = TDictDef(
            '',
            {
                'data': None,
                'info': GetAppVer(),
                'ctrl': {},
                'title': '',
                'route': ''
            }
        )

        self._DoInit()

    def _DoInit(self):
        pass

    async def _DoRender(self):
        pass

    async def _DoSession(self) -> int:
        pass

    async def RegSession(self):
        UserAgent = self.Request.headers.get('User-Agent')
        Parsed = ParseUserAgent(UserAgent)

        Data = await self.ExecCtrl(
            'system/session',
            {
                'method': 'RegSession',
                'param' : {
                    'aBrowser': Parsed['browser'],
                    'aIp': self.Request.remote,
                    'aOs': Parsed['os']
                }
            }
        )

        if ('err' not in Data):
            Dbl = TDbList().Import(Data.get('data'))
            self.Session['session_id'] = Dbl.Rec.id

    async def ExecCtrlDef(self) -> dict:
        return await self.ExecCtrl(f'{self.out.route}')

    async def ExecCtrl(self, aRoute: str, aData: dict = None) -> dict:
        File = self.Tpl.SearchModule(aRoute)
        if (File):
            Source = self.Tpl.Env.loader.LoadFile(File)
            Macro = self.Tpl.ReMacro.findall(Source)
            Extends = [Val.replace('.j2', '') for Key, Val in Macro if Key == 'extends']
        else:
            Extends = []

        Data = {
            'data': aData,
            'route': self.out.route,
            'path_qs': self.Request.path_qs,
            'path': self.Request.path,
            'post': self.out.data,
            'query': dict(self.Request.query),
            'session': dict(self.Session),
            'extends': Extends
        }
        return await self.Ctrl.Get(aRoute, Data)

    async def PostToData(self) -> bool:
        self.out.data.clear()
        if (self.Request.method == 'POST'):
            Post = await self.Request.post()
            self.process(Post)
            if (Post):
                for Key, Val in Post.items():
                    if (isinstance(Val, str)):
                        self.out.data[Key] = Val.strip()
                return bool(Post)

    async def Render(self) -> str:
        self.Session = await get_session(self.Request)
        if (not self.Session.get('start')):
            self.Session['start'] = int(time.time())
            if (not await self._DoSession()):
                await self.RegSession()

        await self.PostToData()

        Res = await self._DoRender()
        if (not Res):
            Res = self.RenderTemplate()
        return Res

    def RenderTemplate(self) -> str:
        Modules = self.RenderModules(self.out.ctrl)
        self.out.ctrl['modules'] = Modules
        self.out.ctrl['places'] = {x['place']: True for x in Modules}

        Data = self.out.ctrl | self.out
        File = f'{self.out.route}.{self.Tpl.Ext}'
        #return self.Tpl.RenderInc(File, Data)
        return self.Tpl.Render(File, Data)

    def RenderModules(self, aData: dict) -> list:
        Res = []
        for xModule in aData.get('modules', []):
            if ('err' not in xModule):
                Layout = xModule['layout']
                Module = Layout['code']
                Route = f'{self.Parent.Conf.form_module}/{Module}.{self.Tpl.Ext}'
                Tpl = self.Tpl.Env.get_template(Route)
                Data = Tpl.render(xModule | Layout)
                Res.append({'data': Data, 'place': Layout['place'], 'name': Module})
        return Res
