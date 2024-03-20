# Created: 2024.03.19
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time


class TIpLog():
    def __init__(self, aInterval: int = 0.5, aCntBanMax: int = 0):
        self.Interval = aInterval
        self.CntBanMax = aCntBanMax

        self.Ip = {}
        self.MaxSize = 1000
        self.IpIgnore = ['127.0.0.1']

    def _CheckSize(self):
        if (len(self.Ip) > self.MaxSize):
            Ten = self.MaxSize // 10
            KeysTen = list(self.Ip.keys())[:Ten]

            for Key in KeysTen:
                del self.Ip[Key]

    def Get(self, aIp: str) -> list:
        return self.Ip.get(aIp)

    def Update(self, aIp: str) -> bool:
        Res = True
        if (self.CntBanMax > 0):
            self._CheckSize()
            if (aIp in self.Ip):
                CntBan, Cnt, Trust, Time = self.Ip[aIp]
                Cnt += 1
                if (not Trust) and (time.time() - Time < self.Interval):
                    CntBan += 1
                    if (CntBan >= self.CntBanMax):
                        CntBan = 0
                        Res = False
                self.Ip[aIp] = [CntBan, Cnt, Trust, time.time()]
            else:
                Trust = aIp in self.IpIgnore
                self.Ip[aIp] = [0, 0, Trust, time.time()]
        return Res
