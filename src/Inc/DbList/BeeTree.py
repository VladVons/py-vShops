# Created: 2022.10.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://blog.boot.dev/computer-science/binary-search-tree-in-python/


class TBeeTree():
    def __init__(self, aData = None):
        self.Left: TBeeTree = None
        self.Right: TBeeTree = None
        self.Data = aData

    def _Asc(self, aTrick: list):
        if (self.Left):
            yield from self.Left._Asc(aTrick)

        if (self.Data):
            if (self.Data[1] == aTrick[0]):
                aTrick[0] = -1
            if (aTrick[0] == -1):
                yield self.Data[1]

        if (self.Right):
            yield from self.Right._Asc(aTrick)

    def Asc(self, aStart: int = -1):
        PassInByRefTrick = [aStart]
        yield from self._Asc(PassInByRefTrick)

    def Add(self, aData: tuple):
        if (self.Data is None):
            self.Data = aData
        elif (self.Data != aData):
            if (aData[0] < self.Data[0]):
                if (self.Left):
                    self.Left.Add(aData)
                else:
                    self.Left = TBeeTree(aData)
            else:
                if (self.Right):
                    self.Right.Add(aData)
                else:
                    self.Right = TBeeTree(aData)

    def Search(self, aVal):
        if (aVal == self.Data[0]):
            Res = self.Data[1]
        elif (aVal < self.Data[0]):
            if (self.Left):
                Res = self.Left.Search(aVal)
            else:
                Res = -self.Data[1]
        else:
            if (self.Right):
                Res = self.Right.Search(aVal)
            else:
                Res = -self.Data[1]
        return Res

    def GetMax(self):
        Cur = self
        while (Cur.Right):
            Cur = Cur.Right
        return Cur.Data[1]

    def GetMin(self):
        Cur = self
        while (Cur.Left):
            Cur = Cur.Left
        return Cur.Data[1]
