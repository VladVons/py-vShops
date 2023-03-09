# Created: 2017.02.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Util.Time import GetDate, GetTime


class TEcho():
    # iex - Info, Error, eXception, Debug
    def __init__(self, aLevel: int = 1, aType: str = 'iexd'):
        self.Level = aLevel
        self.Type = aType
        self.Fmt = ['d', 't', 'c', 'aL', 'aT', 'aM', 'aD', 'aE']

    def _Format(self, aArgs: dict) -> str:
        #Arr = [x + ':' +str(aArgs.get(x, '')) for x in self.Fmt]
        #Arr = [str(aArgs.get(x, '')) for x in self.Fmt]
        Arr = []
        for x in self.Fmt:
            Val = aArgs.get(x)
            if (Val):
                Arr.append(str(Val))
        return ', '.join(Arr)

    def _Write(self, aMsg: str):
        raise NotImplementedError()

    def Write(self, aArgs: dict):
        if (aArgs.get('aL', 0) <= self.Level) and (aArgs.get('aT', 'i') in self.Type):
            Msg = self._Format(aArgs)
            self._Write(Msg)


class TEchoConsole(TEcho):
    def _Write(self, aMsg: str):
        print(aMsg)


class TEchoFile(TEcho):
    def __init__(self, aName: str):
        super().__init__()
        self.Name = aName

    def _Write(self, aMsg: str):
        with open(self.Name, 'a+', encoding='utf-8') as F:
            F.write(aMsg + '\n')


class TLog():
    def __init__(self, aEchoes: list = None):
        self.Cnt = 0
        if (aEchoes is None):
            self.Echoes = []
        else:
            self.Echoes = aEchoes

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
        if (aData is None):
            aData = []
        if (aSkipEcho is None):
            aSkipEcho = []

        self.Cnt += 1
        Args = {'aL': aLevel, 'aT': aType, 'aM': aMsg, 'aD': aData, 'aE': aE, 'c': self.Cnt, 'd': GetDate(), 't': GetTime()}
        self._Write(Args, aSkipEcho)
