# Created:     2021.02.18
# Author:      Vladimir Vons <VladVons@gmail.com>
# License:     GNU, see LICENSE for more details
#
# THyster(+1.2/-0.5)
# Th.Check(10, 11.1)


class THyster():
    def __init__(self, aHyst: float = 1.0):
        self.H = aHyst
        self.On = False

    # Plus only
    def CheckP(self, aKeep: float, aCur: float) -> bool:
        if (aCur < aKeep):
            self.On = True
        elif (aCur >= aKeep + self.H):
            self.On = False
        return self.On


    # # Plus & Minus
    # def CheckPM(self, aKeep: float, aCur: float) -> bool:
    #     if (self.H > 0):
    #         if (aCur < aKeep):
    #             self.On = True
    #         elif (aCur >= aKeep + self.H):
    #             self.On = False
    #     else:
    #         if (aCur > aKeep):
    #             self.On = True
    #         elif (aCur <= aKeep + self.H):
    #             self.On = False
    #     return self.On



    # def CheckMidPM(self, aKeep: float, aCur: float) -> bool:
    #     Hyst = abs(self.H)

    #     if (aCur <= aKeep - Hyst):
    #         self.On = self.H > 0
    #     elif (aCur >= aKeep + Hyst):
    #         self.On = self.H < 0
    #     return self.On
