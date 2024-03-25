# Created: 2023.03.25
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# how to get groupId:
# https://www.youtube.com/watch?v=Pj8mwuMZZvg&ab_channel=Tyrone
#
# from group type /start
# https://api.telegram.org/botXXX/getUpdates
#

# from aiogram import Bot - stucks, so write using lightweight API
import aiohttp


class TTelegram():
    def __init__(self, aToken: str):
        self.Url = f'https://api.telegram.org/bot{aToken}'

    async def _Post(self, aMethod: str, aData: dict) -> object:
        async with aiohttp.ClientSession() as Session:
            try:
                Url = f'{self.Url}/{aMethod}'
                async with Session.post(Url, data=aData) as Response:
                    Data = await Response.read()
                    Res = {'data': Data, 'status': Response.status}
            except Exception as E:
                Res = {'err': str(E)}
            return Res

    async def MessageToGroup(self, aChatId: int, aText: str, aMode: str = 'TEXT'):
        Res =  await self._Post('sendMessage', {
                'chat_id': aChatId,
                'text': aText,
                'parse_mode': aMode
            }
        )
        return Res
