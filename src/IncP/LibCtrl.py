# Created: 2023.03.12
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import re

# pylint: skip-file
from Inc.DbList import TDbList, TDbSql, TDbRec
from Inc.Misc.Crypt import GetCRC
from Inc.Misc.Image import TImage
from Inc.Misc.Pagination import TPagination
from Inc.Misc.Request import TDownload, TRequestGet
from Inc.Misc.RequestImage import TDownloadImage
from Inc.Misc.Telegram import TTelegram
from Inc.Misc.Template import TDictRepl
from Inc.SrvWeb.Common import UrlEncode, UrlUdate
from Inc.Util.Obj import DeepGet, DeepGetByList, GetDictDef, GetDictDefs, Filter, DeepGetsRe, Iif, IsDigits
from Inc.Util.Str import Replace
from .Log import Log


#from jinja2 import Environment, Undefined
#Env = Lib.TplEnvIgnore()
#Product['descr'] = Env.from_string(Product['descr']).render(Res)
# class TplEnvIgnore(Environment):
#     class _TplIgnore(Undefined):
#         def _fail_with_undefined_error(self, *args, **kwargs):
#             return f'?{self._undefined_name}?'

#     def __init__(self):
#         super().__init__(undefined=self._TplIgnore)


class TDictReplDeep(TDictRepl):
    def _VarTpl(self):
        self.ReVar = re.compile(r'(\{\{[a-zA-Z0-9_.]+\}\})')

    def _Get(self, aFind: str) -> str:
        aFind = aFind.strip('{}')
        Res = DeepGet(self.Dict, aFind)
        if (not isinstance(Res, (str, int, float))):
           Res = f'-{aFind}-'
        return Res

def HtmlEsc(aVal: str) -> str:
    return Replace(aVal,
        {
            "'": '&#39;',
            '"': '&quot;',
            '&': '&amp;'
        }
    )

def ResGetModule(aData: dict, aName: str) -> dict:
    for x in aData['res']['modules']:
        if (x['layout']['code'] == aName):
            return x
    return {}

def ResGetLang(aData: dict, aName: str) -> str:
    return aData['res']['lang'].get(aName, aName)

def ResGetItem(aData: dict, aName: str) -> str:
    return aData['res'].get(aName, '')

def AttrDecode(aVal: str) -> dict:
    Res = {}
    if (aVal):
        for Group in aVal.strip('[]').split(';;'):
            if (Group):
                Pair = Group.split(':')
                if (len(Pair) == 2):
                    AttrId, Val = Pair
                    if (AttrId.isdigit()):
                        Res[AttrId] = Val.split(';')
    return Res

async def TelegramMessage(self, aMsg: str) -> object:
    DbConf = self.Cache.Get('conf_tenant_0', {})
    BotToken = DbConf['telegram_bot_token']
    GroupId = DbConf['telegram_group_id']
    Telegram = TTelegram(BotToken)
    return await Telegram.MessageToGroup(GroupId, aMsg, 'HTML')


async def SeoEncodeList(self, aPaths: list[str]) -> list[str]:
    if (aPaths):
        return await self.ApiCtrl.ExecApi(
            'seo',
            {
                'path': aPaths,
                'method': 'Encode'
            }
        )

async def SeoEncodeDict(self, aHref: dict) -> dict:
    Res = await SeoEncodeList(self, aHref.values())
    return dict(zip(aHref.keys(), Res))

async def SeoEncodeStr(self, aHref: str) -> str:
    Res = await SeoEncodeList(self, [aHref])
    return Res[0]

def GetPkgFile(aPkg: str, aFile: str) -> str:
    return aPkg.replace('.', '/') + '/' + aFile

def HideDigit(aVal: int) -> str:
    if (aVal > 10):
        aVal = '>10'
    elif (aVal > 5):
        aVal = '>5'
    elif (aVal > 1):
        aVal = '>1'
    else:
        aVal = str(aVal)
    return aVal
