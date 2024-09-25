# Created: 2024.09.25
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re
import gzip
import shutil
#
from .Echo import TEcho


class TEchoFileGz(TEcho):
    def __init__(self, aName: str):
        super().__init__()
        self.Name = aName
        self.MaxSize = 1_000_000

    def _GetNextExtFile(self, aExt = 'gz'):
        Dir, File = os.path.split(self.Name)

        Files = os.listdir(Dir)
        Indexes = [0]
        for xFile in Files:
            Match = re.search(rf'{File}\.(\d+)\.{aExt}$', xFile)
            if (Match):
                Indexes.append(int(Match.group(1)))
        Next = max(Indexes) + 1
        Res = f'{self.Name}.{Next}.{aExt}'
        return Res

    def _Write(self, aMsg: str):
        with open(self.Name, 'a+', encoding='utf-8') as F:
            F.write(aMsg + '\n')

        if (os.path.getsize(self.Name) > self.MaxSize):
            FileOut = self._GetNextExtFile()
            with open(self.Name, 'rb+') as FIn:
                with gzip.open(FileOut, 'wb') as FOut:
                    FOut.writelines(FIn)
                FIn.truncate(0)

