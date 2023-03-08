# Created: 2023.03.03
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from wtforms import Form
from jinja2.environment import Template
from aiohttp import web
from aiohttp_session import Session, get_session
from multidict import MultiDict
#
from Inc.Conf import TDictDef
from Inc.DataClass import DDataClass
from IncP import GetAppVer
from IncP.Log import Log


@DDataClass
class TFormData():
    title: str
    info: dict
    control: TDictDef = TDictDef('')
    data: TDictDef = TDictDef('')
    data_api: dict = {}


class TFormBase(Form):
    def __init__(self, aRequest: web.Request, aTemplate: Template):
        super().__init__()

        self.Request = aRequest
        self.Template = aTemplate
        self.Post: MultiDict = None
        self.Session: Session = None

        self.out = TFormData(
            info = GetAppVer(),
            title = aTemplate.filename
        )

        self._DoInit()

    def _DoInit(self):
        pass

    async def _DoRender(self):
        pass

    def PostToForm(self) -> bool:
        self.out.data.clear()
        Res = bool(self.Post)
        if (Res):
            for Key, Val in self.Post.items():
                if (isinstance(Val, str)):
                    self.out.data[Key] =  Val.strip()
        return Res

    async def Render(self) -> str:
        self.Session = await get_session(self.Request)

        if (self.Request.method == 'POST'):
            self.Post = await self.Request.post()
            self.process(self.Post)

        Res = await self._DoRender()
        if (Res is None):
            try :
                Res = self.RenderTemplate()
            except Exception as E:
                Msg = 'Render(), %s %s' % (self.Template.filename, E)
                Log.Print(1, 'x', Msg, aE = E)
        return Res

    def RenderTemplate(self) -> str:
        return self.Template.render(out = self.out)
