# Created: 2023.03.03
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
from wtforms import Form
from jinja2.environment import Template
from aiohttp import web
from aiohttp_session import Session, get_session
#
from Inc.Conf import TDictDef
from Inc.DataClass import DDataClass
from Inc.DbList import TDbList
from Inc.Loader.Api import TLoaderApi
from Inc.SrvWeb.Common import ParseUserAgent
from IncP import GetAppVer


@DDataClass
class TFormData():
    title: str
    info: dict
    control: TDictDef
    data: TDictDef
    module: str = ''


class TFormBase(Form):
    '''
        Base class for rendering string from templates
    '''

    def __init__(self, aCtrl: TLoaderApi, aRequest: web.Request, aTemplate: Template):
        super().__init__()

        self._Ctrl = aCtrl
        self.Request = aRequest
        self.Template = aTemplate
        self.Session: Session = None

        self.out = TFormData(
            title = aTemplate.filename,
            info = GetAppVer(),
            control = TDictDef(''),
            data = TDictDef('')
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
            'system',
            {
                'method': 'RegSession',
                'param' : {
                    'aIp': self.Request.remote,
                    'aOs': Parsed['os'],
                    'aBrowser': Parsed['browser']
                }
            }
        )

        if ('err' not in Data):
            Dbl = TDbList().Import(Data.get('data'))
            self.Session['session_id'] = Dbl.Rec.GetField('id')

    async def ExecCtrlDef(self) -> dict:
        return await self.ExecCtrl(self.out.module)

    async def ExecCtrl(self, aModule: str, aData: dict = None) -> dict:
        Data = {
            'query': dict(self.Request.query),
            'post': self.out.data,
            'path': self.Request.path,
            'path_qs': self.Request.path_qs,
            'data': aData,
            'session': dict(self.Session)
        }
        return await self._Ctrl.Get(aModule, Data)

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
        return self.Template.render(out = self.out)
