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
