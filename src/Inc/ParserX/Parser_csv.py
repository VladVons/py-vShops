# Created: 2022.09.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import csv
#
from .Common import TEngine


class TParser_csv(TEngine):
    def _InitEngine(self, aFile: str):
        return True

    async def _Load(self):
        ConfEncoding = self.Parent.Conf.get('encoding', 'cp1251')
        ConfDelim = self.Parent.Conf.get('delimiter', ',')

        ConfSheet = self.GetConfSheet()
        ConfFields = ConfSheet.get('fields')
        ConfSkip = ConfSheet.get('skip', 0)
        ConfFile = self.Parent.GetFile()

        with open(ConfFile, 'r',  encoding=ConfEncoding, errors='ignore') as File:
            Data = csv.reader(File, delimiter = ConfDelim)
            for _i in range(ConfSkip):
                next(Data)

            for RowNo, Row in enumerate(Data, ConfSkip):
                Data = {'No': RowNo}
                for Field, FieldIdx in ConfFields.items():
                    Val = Row[FieldIdx - 1]
                    Data[Field] = Val
                self._Fill(Data)
                await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
