# Created: 2023.07.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from Inc.DbList import TDbList
from .Common import TEngine


class TParser_dbl(TEngine):
    def _InitEngine(self, aFile: str):
        ConfEncoding = self.Parent.Conf.get('encoding', 'utf8')
        with open(aFile, 'r', encoding=ConfEncoding) as F:
            return json.load(F)

    async def _Load(self):
        assert(self._Engine), f'InitEngine() not invoked {self.GetFile()}'

        assert(self._Sheet in self._Engine), f'Sheet not found {self._Sheet}'
        WSheet = self._Engine[self._Sheet]
        Dbl = TDbList().Import(WSheet)

        for RowNo, Rec in enumerate(Dbl):
            Data = {'no': RowNo}
            Data.update(Rec.GetAsDict())
            self._Fill(Data)
            await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
