# Created: 2021.02.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://github.com/kipe/pycron
# https://crontab.guru/examples.html
#
# Sec     Min     Hour    Day     Month   DOW
# *       */3     6,8-20  *       *       *
# IsNow('* */3 6,8-20 * * 2')


import time


def _Parse(aValue: str, aTarget: int) -> bool:
    for Value in aValue.split(','):
        # *
        if (aValue == '*'):
            return True

        # 3-5
        if ('-' in Value):
            Start, End = Value.split('-')
            if (int(Start) <= aTarget <= int(End)):
                return True
        # */3
        elif ('/' in Value):
            _, Step = Value.split('/')
            if (aTarget % int(Step) == 0):
                return True
        # 2
        elif (aTarget == int(Value)):
            return True
    return False

def IsNow(aPattern: str) -> bool:
    _YearT, MonthT, DOMT, HourT, MinT, SecT, DOWT, *_X = time.localtime(time.time())
    Sec, Min, Hour, DOM, Month, DOW = aPattern.split(' ')

    Res = _Parse(Sec, SecT) and \
          _Parse(Min, MinT) and \
          _Parse(Hour, HourT) and \
          _Parse(DOM, DOMT) and \
          _Parse(Month, MonthT) and \
          _Parse(DOW, DOWT)
    return Res


class TCron():
    #Data = [('* */2 8-13 * * *', 22), ('* * 14-23 * * *', 24)]
    def __init__(self, aData = None):
        if (aData is None):
            aData = []

        self.Data = aData

    async def Get(self):
        for Cron, Val in self.Data:
            if (IsNow(Cron)):
                return Val
