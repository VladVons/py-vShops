# Created: 2017.02.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


class TEcho():
    # iex - Info, Error, eXception, Debug
    def __init__(self, aLevel: int = 1, aType: str = 'iexd'):
        self.Level = aLevel
        self.Type = aType
        self.Fmt = ['d', 't', 'c', 'aL', 'aT', 'aM', 'aD', 'aE']
        #self.Fmt = '{d} {t}, {c}, {aL}, {aT}, {aM}, {aD}, {aE}'


    def _Format(self, aArgs: dict) -> str:
        if (isinstance(self.Fmt, list)):
            Arr = [str(aArgs[x]) for x in self.Fmt if aArgs.get(x)]
            Res = ', '.join(Arr)
        else:
            Res = self.Fmt.format(**aArgs)
        return Res

    def _Write(self, aMsg: str):
        raise NotImplementedError()

    def Write(self, aArgs: dict):
        if (aArgs.get('aL', 0) <= self.Level) and (aArgs.get('aT', 'i') in self.Type):
            Msg = self._Format(aArgs)
            self._Write(Msg)
