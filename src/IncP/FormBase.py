# Created: 2023.03.03
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from wtforms import Form
from jinja2.environment import Template
from aiohttp import web
from aiohttp_session import Session, get_session
#
from Inc.Conf import TDictDef
from Inc.DataClass import DDataClass
from IncP import GetAppVer


@DDataClass
class TFormData():
    title: str
    path: str
    info: dict
    control: TDictDef
    data: TDictDef
    data_api: dict


class TFormBase(Form):
    '''
        Base class for rendering string from templates
    '''

    def __init__(self, aRequest: web.Request, aTemplate: Template):
        super().__init__()

        self.Request = aRequest
        self.Template = aTemplate
        self.Session: Session = None

        self.out = TFormData(
            title = aTemplate.filename,
            path = aRequest.path,
            info = GetAppVer(),
            control = TDictDef(''),
            data = TDictDef(''),
            data_api = {}
        )

        self._DoInit()

    def _DoInit(self):
        pass

    async def _DoRender(self):
        pass

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
        await self.PostToData()

        Res = await self._DoRender()
        if (Res is None):
            Res = self.RenderTemplate()
        return Res

    def RenderTemplate(self) -> str:
        return self.Template.render(out = self.out)
