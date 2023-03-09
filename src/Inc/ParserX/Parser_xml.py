# Created: 2023.02.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import xml.dom.minidom as dom
#
from .Common import TEngine


class TParser_xml(TEngine):
    def _InitEngine(self, aFile: str):
        ConfEncoding = self.Parent.Conf.get('encoding')
        with open(aFile, 'r', encoding=ConfEncoding) as F:
            return dom.parse(F)

    async def _Load(self):
        assert self._Engine, 'InitEngine() not invoked %s' % self.GetFile()

        Nodes = self._Engine.getElementsByTagName(self._Sheet)
        for Row in Nodes:
            self._Fill(Row)
            await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
