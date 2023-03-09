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
        Conf = self.GetConfSheet()
        ConfFields = Conf.get('fields')
        ConfSkip = Conf.get('skip', 3)
        ConfEncoding = Conf.get('encoding', 'cp1251')
        ConfFile = self.Parent.GetFile()

        with open(ConfFile, 'r',  encoding=ConfEncoding, errors='ignore') as File:
            Data = csv.reader(File, delimiter = ',')
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
