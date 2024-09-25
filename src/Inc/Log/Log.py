# Created: 2017.02.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Time import GetDate, GetTime
from .Echo import TEcho


class TLog():
    def __init__(self, aEchoes: list = None):
        self.Echoes = aEchoes or []
        self.Cnt = 0
        self.MsgUniq = False
        self.MsgLast = None

    def _Write(self, aData: dict, aSkipEcho: list):
        for Echo in self.Echoes:
            if (Echo.__class__.__name__ not in aSkipEcho):
                Echo.Write(aData)

    def FindEcho(self, aClassName: str) -> list:
        #return list(filter(lambda i: (i.__class__.__name__ == aClassName), self.Echoes))
        return [i for i in self.Echoes if (i.__class__.__name__ == aClassName)]

    def AddEcho(self, aEcho: TEcho):
        Name = aEcho.__class__.__name__
        if (not self.FindEcho(Name)):
            self.Echoes.append(aEcho)

    def Print(self, aLevel: int, aType: str, aMsg: str, aData: list = None, aE: Exception = None, aSkipEcho: list = None):
        self.Cnt += 1

        if (self.MsgUniq) and (self.MsgLast == aMsg):
            return

        self.MsgLast = aMsg
        aData = aData or []
        aSkipEcho = aSkipEcho or []

        Args = {'aL': aLevel, 'aT': aType, 'aM': aMsg, 'aD': aData, 'aE': aE, 'c': self.Cnt, 'd': GetDate(), 't': GetTime()}
        self._Write(Args, aSkipEcho)
