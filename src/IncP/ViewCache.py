# Created: 2023.03.21
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import time


class TViewCache():
    def __init__(self, aDir: str, aMaxAge: int = 5, aSkipModule: list[str] = None):
        assert (os.path.isdir(aDir)), 'Directory not exists'

        self.Dir = aDir
        self.MaxAge = aMaxAge
        self.SkipModule = aSkipModule

    def _GetPath(self, aModule: str, aQuery: dict) -> str:
        if (aQuery):
            Arr = [f'{Key}:{Val}'for Key, Val in aQuery.items()]
            File = '_'.join(Arr)
        else:
            File = 'index'
        return f'{self.Dir}/{aModule}/{File}.html'

    def Get(self, aModule: str, aQuery: dict) -> str:
        Path = self._GetPath(aModule, aQuery)
        if (os.path.exists(Path)) and (time.time() - os.path.getmtime(Path) < self.MaxAge):
            with open(Path, 'r', encoding='utf-8') as F:
                return F.read()

    def Set(self, aModule: str, aQuery: dict, aData: str):
        if (not self.MaxAge) or ((self.SkipModule) and (aModule in self.SkipModule)):
            return

        Path = self._GetPath(aModule, aQuery)
        Dir = Path.rsplit('/', maxsplit=1)[0]
        if (not os.path.isdir(Dir)):
            os.makedirs(Dir)

        with open(Path, 'w', encoding='utf-8') as F:
            F.write(aData)
