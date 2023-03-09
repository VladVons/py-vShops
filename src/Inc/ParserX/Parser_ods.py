# Created: 2022.09.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from pyexcel_ods import get_data
#
from .Common import TEngine


class TParser_ods(TEngine):
    def _InitEngine(self, aFile: str):
        return get_data(aFile)

    async def _Load(self):
        assert self._Engine, 'InitEngine() not invoked %s' % self.GetFile()

        if (self._Sheet == 'default'):
            Sheet = list(self._Engine.keys())[0]
        else:
            Sheet = self._Sheet

        Conf = self.GetConfSheet()
        ConfSkip = Conf.get('skip', 0)
        ConfFields = Conf.get('fields')

        Rows = self._Engine.get(Sheet)
        for i in range(ConfSkip, len(Rows)):
            Data = {'no': i}
            for Field, (FieldIdx, _) in ConfFields.items():
                Val = Rows[i][FieldIdx - 1]
                Data[Field] = Val
            self._Fill(Data)
            await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
