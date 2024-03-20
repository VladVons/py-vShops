# Created: 2024.03.19
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time


class TIpLog():
    def __init__(self, aInterval: int = 0.5):
        self.Ip = {}
        self.Interval = aInterval
        self.MaxSize = 1000
        self.IpIgnore = ['127.0.0.1']
        self.CntForBan = 5

    def _CheckSize(self):
        if (len(self.Ip) > self.MaxSize):
            Ten = self.MaxSize // 10
            KeysTen = list(self.Ip.keys())[:Ten]

            for Key in KeysTen:
                del self.Ip[Key]

    def Get(self, aIp: str) -> list:
        return self.Ip.get(aIp)

    def Update(self, aIp: str) -> bool:
        self._CheckSize()
        Res = True
        if (aIp in self.Ip):
            CntBan, Cnt, Trust, Time = self.Ip[aIp]
            Cnt += 1
            if (not Trust) and (time.time() - Time < self.Interval):
                CntBan += 1
                if (CntBan >= self.CntForBan):
                    Res = False
            self.Ip[aIp] = [CntBan, Cnt, Trust, time.time()]
        else:
            Trust = aIp in self.IpIgnore
            self.Ip[aIp] = [0, 0, Trust, time.time()]
        return Res
