# Created: 2023.03.03
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from multidict import MultiDict
from wtforms import Form
from jinja2.environment import Template
#
from Inc.Conf import TDictDef
from Inc.DataClass import DDataClass
from IncP import GetAppVer
from IncP.Log import Log


@DDataClass
class TFormData():
    control: TDictDef
    data: TDictDef
    title: str
    info: dict


class TFormBase(Form):
    def __init__(self, aPath: str, aQuery: str, aPostData: MultiDict, aTemplate: Template, aMasterData: dict, aUserData: dict):
        super().__init__()

        self.Path = aPath
        self.Query = aQuery
        self.PostData = aPostData
        self.Template = aTemplate
        self.MasterData = aMasterData

        self.out = TFormData(
            control = TDictDef(''),
            data = TDictDef('', aUserData),
            info = GetAppVer(),
            title = aTemplate.filename
        )

        self._DoInit()

    def _DoInit(self):
        pass

    async def _Render(self):
        pass

    def PostToForm(self) -> bool:
        self.out.data.clear()
        Res = bool(self.PostData)
        if (Res):
            for Key, Val in self.PostData.items():
                if (isinstance(Val, str)):
                    self.out.data[Key] =  Val.strip()
        return Res

    async def Render(self) -> str:
        self.process(self.PostData)

        Res = await self._Render()
        if (Res is None):
            try :
                Res = self.RenderTemplate()
            except Exception as E:
                Msg = 'Render(), %s %s' % (self.Template.filename, E)
                Log.Print(1, 'x', Msg, aE = E)
        return Res

    def RenderTemplate(self) -> str:
        return self.Template.render(out = self.out)
