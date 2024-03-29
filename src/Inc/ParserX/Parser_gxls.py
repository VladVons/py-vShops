# Created: 2023.02.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://console.developers.google.com
# https://docs.gspread.org/en/latest/oauth2.html
# https://www.youtube.com/watch?v=bu5wXjz2KvU


import gspread
#
from .Common import TEngine


class TParser_gxls(TEngine):
    def _InitEngine(self, aFile: str):
        pass

    async def _Load(self):
        assert(self._Engine), f'InitEngine() not invoked {self.GetFile()}'

        #Auth = '~/.config/gspread/service_account.json'
        gsa = gspread.service_account()
        #sh = gsa.open("MySpreadsheetName")
        sh = gsa.open_by_url(Url)
        sh1 = sh.sheet1
        sh.get('A1')

        Nodes = self._Engine.getElementsByTagName(self._Sheet)
        for Row in Nodes:
            self._Fill(Row)
            await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
