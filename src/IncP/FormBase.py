# Created: 2023.03.03
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
from wtforms import Form
from aiohttp import web
from aiohttp.web_request import FileField
from aiohttp_session import Session, get_session
#
from Inc.DbList import TDbList
from Inc.DictDef import TDictDef
from Inc.Loader.Api import TLoaderApi
from Inc.Misc.Jinja import TTemplate
from Inc.Util.Obj import DeepGetByList
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
                'data': {},
                'files': [],
                'info': GetAppVer(),
                'title': '',
                'route': '',
                'path': '',
                'query': {}
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

        #print('-x1', '\n'.join([f'{Key}:{Val}' for Key, Val in self.Request.headers.items()]))
        Remote = self.Request.remote
        if (Remote == '127.0.0.1'):
            # try to get remote ip from nginx proxy (proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;)
            Remote = self.Request.headers.get('X-FORWARDED-FOR', '127.0.0.1')

        Data = await self.ExecCtrl(
            'system/session',
            {
                'method': 'RegSession',
                'param' : {
                    'aBrowser': Parsed['browser'],
                    'aIp': Remote,
                    'aOs': Parsed['os']
                }
            }
        )

        if ('err' not in Data):
            Dbl = TDbList().Import(Data.get('data'))
            self.Session['session_id'] = Dbl.Rec.id

    async def ExecCtrlDef(self) -> dict:
        return await self.ExecCtrl(self.out.route, {'method': 'Main'})

    async def ExecCtrl(self, aRoute: str, aData: dict = None) -> dict:
        File = self.Tpl.SearchModule(aRoute)
        if (File):
            Source = self.Tpl.Env.loader.LoadFile(File)
            Macro = self.Tpl.ReMacro.findall(Source)

            Extends = [
                Val.replace('.j2', '')
                for Key, Val in Macro
                if Key == 'extends'
            ]
        else:
            Extends = []

        Data = {
            'type': 'form',
            'route': self.out.route,
            '_path': self.out.path,
            'path_qs': self.Request.path_qs,
            'path': self.Request.path,
            'post': self.out.data,
            'query': dict(self.Request.query) | self.out.query,
            'session': dict(self.Session),
            'extends': Extends
        }
        if (aData):
            Data.update(aData)
            aRoute = Data.get('route_ctrl', aRoute)

        return await self.Ctrl.Get(aRoute, Data)

    async def PostToData(self) -> bool:
        if (self.Request.method.upper() == 'POST'):
            Post = await self.Request.post()
            self.process(Post)
            if (Post):
                for Key, Val in Post.items():
                    if (isinstance(Val, str)):
                        self.out.data[Key] = Val.strip()
                    elif (isinstance(Val, FileField)):
                        self.out.files.append((Val, Key))

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
        Modules = self.RenderModules(self.out.get('modules', []))
        self.out['modules'] = Modules
        self.out['places'] = {x['place']: True for x in Modules}

        File = f'{self.out.route}.{self.Tpl.Ext}'
        if ('err_code' in self.out):
            File = f'{self.Parent.Conf.form_info}.{self.Tpl.Ext}'
            self.out.info_data = DeepGetByList(self.out, ['lang',  f'err_code_{self.out.err_code}'], 'Unknown error')
        #return self.Tpl.RenderInc(File, Data)
        return self.Tpl.Render(File, self.out)


    def RenderModules(self, aModules: list) -> list:
        Res = []
        for xModule in aModules:
            if ('err' not in xModule):
                Layout = xModule['layout']
                Module = Layout['code']
                Route = f'{self.Parent.Conf.form_module}/{Module}.{self.Tpl.Ext}'
                Tpl = self.Tpl.Env.get_template(Route)
                Data = Tpl.render(xModule | Layout)
                Res.append({'data': Data, 'place': Layout['place'], 'name': Module})
        return Res
