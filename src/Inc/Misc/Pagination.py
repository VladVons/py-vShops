# Created: 2023.12.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# TPagination(15, 'url&page={page}').Get(250,  7)


import math


class TPagination():
    def __init__(self, aPerPage: int, aHref: str):
        self.PerPage = aPerPage
        self.Href = aHref
        self.Back = '&lt;'
        self.Forward = '&gt;'
        self.Visible = 3

    def ToDict(self, aPage: int, aTitle: str, aCurPage: bool = False) -> tuple:
        return (aPage, aTitle, self.Href.format(page=aPage), aCurPage)

    def Get(self, aRecords: int, aCurPage: int) -> list:
        def Loop(aBegin: int, aEnd: int):
            nonlocal Res
            for xPage in range(aBegin, aEnd + 1):
                if (xPage == aCurPage):
                    Res.append(self.ToDict(xPage, xPage, True))
                else:
                    Res.append(self.ToDict(xPage, xPage))

        Pages = math.ceil(aRecords / self.PerPage)
        aCurPage = max(1, min(Pages, aCurPage))
        Begin = max(1, aCurPage - self.Visible // 2)
        End = min(Pages, Begin + self.Visible - 1)

        if (End - Begin + 1 < self.Visible):
            Begin = max(1, End - self.Visible + 1)

        Res = []
        if (Pages > self.Visible + 2):
            if (Begin > 1):
                Res.append(self.ToDict(1, 1))
                if (Begin > 2):
                    Res.append(self.ToDict(Begin - 1, self.Back))
            Loop(Begin, End)
            if (End < Pages):
                if (End < Pages - 1):
                    Res.append(self.ToDict(End + 1, self.Forward))
                Res.append(self.ToDict(Pages, Pages))
        else:
            Loop(1, Pages)
        return Res
