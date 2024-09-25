# Created: 2017.02.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from .Echo import TEcho


class TEchoConsole(TEcho):
    def _Write(self, aMsg: str):
        print(aMsg)
