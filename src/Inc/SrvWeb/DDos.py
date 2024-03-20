# Created: 2024.03.19
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time


class TDDos():
    def __init__(self, aInterval: int = 0.5):
        self.Ip = {}
        self.Interval = aInterval
        self.MaxSize = 1000
        self.IpIgnore = ['127.0.0.1']
        self.CntForBan = 5

    def CheckSize(self):
        if (len(self.Ip) > self.MaxSize):
            Ten = self.MaxSize // 10
            KeysTen = list(self.Ip.keys())[:Ten]

            for Key in KeysTen:
                del self.Ip[Key]

    def Update(self, aIp: str) -> int:
        Res = 0
        if (aIp in self.IpIgnore):
            return Res

        self.CheckSize()
        if (aIp in self.Ip):
            Time, Cnt = self.Ip[aIp]
            if (time.time() - Time < self.Interval):
                Cnt += 1
                Res = Cnt
            elif (Cnt >= self.CntForBan):
                Res = Cnt
        else:
            Cnt = 0
        self.Ip[aIp] = [time.time(), Cnt]
        return Res
