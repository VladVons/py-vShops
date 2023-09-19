# Created: 2023.09.18
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Common import TEngine


class TParser_txt(TEngine):
    def _InitEngine(self, aFile: str):
        return True

    async def _Load(self):
        ConfEncoding = self.Parent.Conf.get('encoding', 'utf8')
        ConfSheet = self.GetConfSheet()
        ConfSkip = ConfSheet.get('skip', 0)
        ConfFile = self.Parent.GetFile()

        with open(ConfFile, 'r',  encoding=ConfEncoding, errors='ignore') as File:
            Lines = File.readlines()

        for RowNo in range(ConfSkip, len(Lines)):
            Data = {'no': RowNo, 'data': Lines[RowNo]}
            self._Fill(Data)
            await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
