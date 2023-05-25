# Created:     2023.01.29
# Author:      Vladimir Vons <VladVons@gmail.com>
# License:     GNU, see LICENSE for more details
#
# Code8 = '42069942'
# Code13 = '4820192681810'
# Ean13 = TEan13(Code13)
# print(Code13, Ean13.Check())
# Ean = TEan()
# print(Code8, Ean.Init(Code8).Check())
# print(Code13, Ean.Init(Code13).Check())


class TEan():
    def __init__(self, aCode: str = ''):
        self.Code = aCode
        self.Len = 0

    def Init(self, aCode: str) -> 'TEan':
        self.Code = aCode
        return self

    def Get(self) -> str:
        return '%s%s' % (self.Code[:-1], self.GetCrc())

    def GetCrc(self) -> int:
        Body = self.Code[:-1]
        #Data = [(3 if i % 2 == 0 else 1) * int(x) for i, x in enumerate(reversed(Body))]
        Data = [(3, 1)[i % 2] * int(x) for i, x in enumerate(reversed(Body))]
        return (10 - sum(Data)) % 10

    def Check(self) -> bool:
        return  (self.Code) and \
                (self.Len == 0 or self.Len == len(self.Code)) and \
                (self.Code.isdigit()) and \
                (self.Code[-1] == str(self.GetCrc()))

class TEan8(TEan):
    Len = 8

class TEan13(TEan):
    Len = 13
