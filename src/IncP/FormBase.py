# Created: 2023.03.03
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
from wtforms import Form
from jinja2.environment import Template
from aiohttp import web
from aiohttp_session import Session, get_session
#
from Inc.DbList import TDbList
from Inc.DictDef import TDictDef
from Inc.Loader.Api import TLoaderApi
from Inc.SrvWeb.Common import ParseUserAgent
from IncP import GetAppVer


class TFormBase(Form):
    '''
        Base class for rendering string from templates
    '''

    def __init__(self, aCtrl: TLoaderApi, aRequest: web.Request, aTemplate: Template):
        super().__init__()

        self.Ctrl = aCtrl
        self.Request = aRequest
        self.Template = aTemplate
        self.Session: Session = None

        self.out = TDictDef(
            '',
            {
                'data': {},
                'info': GetAppVer(),
                'modules': {},
                'title': aTemplate.filename
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
        return await self.ExecCtrl(f'route/{self.out.module}')

    async def ExecCtrl(self, aModule: str, aData: dict = None) -> dict:
        Data = {
            'data': aData,
            'module': aModule,
            'path_qs': self.Request.path_qs,
            'path': self.Request.path,
            'post': self.out.data,
            'query': dict(self.Request.query),
            'route': self.out.module,
            'session': dict(self.Session)
        }
        return await self.Ctrl.Get(aModule, Data)

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
        return self.Template.render(**self.out)
