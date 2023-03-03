# Created: 2022.02.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# see also
# https://github.com/alexmic/microtemplates


from aiohttp import web
from aiohttp_jinja2 import render_template
from wtforms import Form
#
from Inc.DictDef import TDictDef
from Inc.DataClass import DDataClass
from IncP import GetAppVer
from IncP.Log import Log
from ..Session import Session


@DDataClass
class TFormData():
    control: TDictDef
    data: TDictDef
    title: str
    info: dict


class TFormBase(Form):
    def __init__(self, aRequest: web.Request, aTpl: str, aData: dict = None):
        super().__init__()

        self.Request = aRequest
        self.Tpl = aTpl
        self.Parent = None

        self.out = TFormData(
            control = TDictDef(''),
            data = TDictDef('', aData),
            info = GetAppVer(),
            title = aTpl.split('.')[0]
        )

        self._DoInit()

    def _DoInit(self):
        pass

    async def PostToForm(self):
        self.out.control.clear()
        Post = await self.Request.post()
        for Key, Val in Post.items():
            if (isinstance(Val, str)):
                self.out.control[Key] = Val.strip()
        return bool(Post)

    async def Render(self) -> web.Response:
        self.process(await self.Request.post())

        await Session.Update(self.Request)
        #if (Session.CheckUserAccess(self.Request.path)):
        Res = await self._Render()
        if (Res is None):
            try :
                Res = self.RenderTemplate()
            except Exception as E:
                Msg = 'Render(), %s %s' % (self.Tpl, E)
                Log.Print(1, 'x', Msg, aE = E)
                Res = self.RenderInfo(Msg)
        #else:
        #    Msg = 'Access denied %s %s. Policy interface_allow' % (self.Request.path, Session.Data.get('UserName'))
        #    Res = self.RenderInfo(Msg)
        return Res

    def RenderTemplate(self):
        return render_template(self.Tpl, self.Request, {'out': self.out})

    def RenderInfo(self, aMsg: str) -> web.Response:
        self.out.data['info'] = aMsg
        return render_template('info.tpl', self.Request, {'out': self.out})

    async def _Render(self):
        #print('_Render() not implemented for %s' % (self.Tpl))
        pass
