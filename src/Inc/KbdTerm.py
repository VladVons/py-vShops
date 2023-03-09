# Created: 2021.02.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


try:
    import asyncio
except ModuleNotFoundError:
    import uasyncio as asyncio

import sys
import select


class TKbdTerm():
    '''
    def __init__(self):
        self.Poller = select.poll()
        self.Poller.register(sys.stdin, select.POLLIN)
        pass

    #rst cause:4, boot mode:(3,6)
    def GetChr(self):
        for s, ev in self.Poller.poll(500):
            return s.read(1)
    '''

    def GetChr(self) -> str:
        R = ''
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            R = sys.stdin.read(1)
        return R


    async def Input(self, aPrompt = '') -> str:
        sys.stdout.write('%s%s   \r' % (aPrompt, ''))

        R = ''
        while True:
            K = self.GetChr()
            if (K):
                if (ord(K) == 10): # enter
                    print()
                    return R

                if (ord(K) == 27): # esc
                    return ''

                if (ord(K) == 127): # bs
                    R = R[:-1]
                else:
                    R += K
                sys.stdout.write('%s%s   \r' % (aPrompt, R))
            await asyncio.sleep(0.5)
