# Created: 2022.09.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from openpyxl import load_workbook
#
from .Common import TEngine


class TParser_xlsx(TEngine):
    def _InitEngine(self, aFile: str):
        return load_workbook(aFile, read_only = True, data_only = True)

    async def _Load(self):
        assert(self._Engine), f'InitEngine() not invoked {self.GetFile()}'

        if (self._Sheet == 'default'):
            WSheet = self._Engine.active
        else:
            WSheet = self._Engine[self._Sheet]

        Conf = self.GetConfSheet()
        ConfFields = Conf.get('fields')
        ConfSkip = Conf.get('skip', 0)
        for RowNo, Row in enumerate(WSheet.rows):
            if (RowNo >= ConfSkip):
                Data = {'no': RowNo}
                for Field, FieldIdx in ConfFields.items():
                    Val = Row[FieldIdx - 1].value
                    Data[Field] = Val
                self._Fill(Data)
                await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
