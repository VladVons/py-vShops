# Created: 2023.09.04
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
#
from Inc.DataClass import DDataClass
from Inc.Util.Obj import GetTree
from IncP import GetSysInfo, DictToText
from IncP.Log import Log
from Task.SrvCtrl import ApiCtrl


@DDataClass
class TTelegramConf():
    token: str

class TTelegram():
    def __init__(self, aConf: TTelegramConf):
        self.Conf = aConf
        self.Bot: Bot

    async def cmd_start(self, aMsg: types.Message):
        Keyboard = [
            [types.KeyboardButton(text = '/AppInfo'), types.KeyboardButton(text = '/DbInfo')],
            [types.KeyboardButton(text = '/Echo')]

        ]
        ReplyMarkup = types.ReplyKeyboardMarkup(keyboard=Keyboard, resize_keyboard=True)
        await aMsg.answer('=cmd_start=', reply_markup=ReplyMarkup)

    async def cmd_AppInfo(self, aMsg: types.Message):
        Data = GetSysInfo()
        await aMsg.answer(DictToText(Data))

    async def cmd_DbInfo(self, aMsg: types.Message):
        Data = await ApiCtrl.Exec('misc/about', {'method': 'Main', 'type': 'api'})
        Arr = [f"{x[1].lstrip('/')}: {x[2]}" for x in GetTree(Data['data'])]
        #await self.Bot.send_message(message.chat.id, 'Hello 123')
        await aMsg.answer('\n'.join(Arr))

    async def cmd_Echo(self, aMsg: types.Message):
        await aMsg.reply("Напиши мне что-нибудь")
        #await self.Bot.send_message(aMsg.from_user.id, f'echo: {aMsg.text}')

    # async def cmd_Query(self, aQuery: types.InlineQuery):
    #     input_content = types.InputTextMessageContent(aQuery.query or 'echo')
    #     item = types.InlineQueryResultArticle(id='1', title='echo', input_message_content=input_content)
    #     await self.Bot.answer_inline_query(aQuery.id, results=[item], cache_time=1)

    async def Run(self):
        Log.Print(1, 'i', 'Telegram.RunApp()')

        dp = Dispatcher()
        dp.message.register(self.cmd_start, Command('start'))
        dp.message.register(self.cmd_AppInfo, Command('AppInfo'))
        dp.message.register(self.cmd_DbInfo, Command('DbInfo'))
        dp.message.register(self.cmd_Echo, Command('Echo'))
        # dp.inline_query.register(self.cmd_Query)

        self.Bot = Bot(self.Conf.token)
        await dp.start_polling(self.Bot)
