# Created: 2023.03.12
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


# pylint: skip-file
from Inc.DbList import TDbList, TDbSql, TDbRec
from Inc.Misc.Crypt import GetCRC
from Inc.Misc.Image import TImage
from Inc.Misc.Pagination import TPagination
from Inc.Misc.Request import TDownload, TDownloadImage
from Inc.Misc.Telegram import TTelegram
from Inc.SrvWeb.Common import UrlEncode, UrlUdate
from Inc.Util.Obj import DeepGetByList, GetDictDef, GetDictDefs, Filter, DeepGetsRe, Iif, IsDigits
from Inc.Util.Str import Replace
from .Log import Log


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
    return aData['res']['lang'].get(aName, '')

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
