# Created: 2022.09.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from xlrd import open_workbook
#
from .Common import TEngine


class TParser_xls(TEngine):
    def _InitEngine(self, aFile: str):
        return open_workbook(aFile)

    async def _Load(self):
        assert self._Engine, 'InitEngine() not invoked %s' % self.GetFile()

        if (self._Sheet == 'default'):
            WS = self._Engine.sheet_by_index(0)
        else:
            WS = self._Engine.sheet_by_name(self._Sheet)

        Conf = self.GetConfSheet()
        ConfFields = Conf.get('fields')
        ConfSkip = Conf.get('skip', 0)
        for i in range(ConfSkip, WS.nrows):
            Data = {'no': i}
            for Field, FieldIdx in ConfFields.items():
                Val = WS.cell(i, FieldIdx - 1).value
                Data[Field] = Val
            self._Fill(Data)
            await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
