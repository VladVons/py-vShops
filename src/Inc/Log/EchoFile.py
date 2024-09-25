# Created: 2024.09.25
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from . import TEcho


class TEchoFile(TEcho):
    def __init__(self, aName: str):
        super().__init__()
        self.Name = aName

    def _Write(self, aMsg: str):
        with open(self.Name, 'a+', encoding='utf-8') as F:
            F.write(aMsg + '\n')
