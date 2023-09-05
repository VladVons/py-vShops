# Created: 2023.09.04
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
#
from Inc.DataClass import DDataClass
from Inc.Util.Obj import GetTree
from IncP.Log import Log
from Task.SrvCtrl import ApiCtrl


@DDataClass
class TTelegramConf():
    token: str

class TTelegram():
    def __init__(self, aConf: TTelegramConf):
        self.Conf = aConf
        self.Bot: Bot

    async def cmd_start(self, message: types.Message):
        Keyboard = [
            [types.KeyboardButton(text = '/DbInfo')]
        ]
        ReplyMarkup = types.ReplyKeyboardMarkup(keyboard=Keyboard, resize_keyboard=True)
        await message.answer('=cmd_start=', reply_markup=ReplyMarkup)

    async def cmd_DbInfo(self, message: types.Message):
        Data = await ApiCtrl.Exec('misc/about', {'method': 'Main', 'type': 'api'})
        Arr = [f"{x[1].lstrip('/')}: {x[2]}" for x in GetTree(Data['data'])]
        #await self.Bot.send_message(message.chat.id, 'Hello 123')
        await message.answer('\n'.join(Arr))

    async def Run(self):
        Log.Print(1, 'i', 'Telegram.RunApp()')

        dp = Dispatcher()
        dp.message.register(self.cmd_start, Command('start'))
        dp.message.register(self.cmd_DbInfo, Command('DbInfo'))
        self.Bot = Bot(self.Conf.token)
        await dp.start_polling(self.Bot)
