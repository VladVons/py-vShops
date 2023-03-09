# Created: 2023.02.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://docs.gspread.org/en/latest/oauth2.html


import gspread
#
from .Common import TEngine


class TParser_gxls(TEngine):
    def _InitEngine(self, aFile: str):
        pass

    async def _Load(self):
        assert self._Engine, 'InitEngine() not invoked %s' % self.GetFile()

        # ToDo
        gsa = gspread.service_account()
        sh = gsa.open("Example spreadsheet")
        sh1 = sh.sheet1
        sh.get('A1')

        Nodes = self._Engine.getElementsByTagName(self._Sheet)
        for Row in Nodes:
            self._Fill(Row)
            await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
