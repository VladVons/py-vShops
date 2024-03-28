# Created: 2023.12.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# Data = TPagination(15, 'url', '&page={page}').Get(250,  7)
# for (PageNo, Title, Href, IsActive) in Data:
#     print(f'{IsActive = :1}, {PageNo = :3}, {Href = :11}, {Title = }')


import math
import re


class TPagination():
    def __init__(self, aPerPage: int, aHref: str, aPager: str = '&page={page}'):
        self.PerPage = aPerPage
        self.Href = re.sub(aPager.replace('{page}', r'\d+'), '', aHref)
        self.Pager = aPager
        self.Back = '&lt;'
        self.Forward = '&gt;'
        self.Visible = 3

    def ToTuple(self, aPage: int, aTitle: str, aCurPage: bool = False) -> tuple:
        Href = self.Href
        if (aPage > 1):
            if ('?' in Href):
                Href += self.Pager
            else:
                Href = '?' + self.Pager[1:]
        Res = (aPage, aTitle, Href.format(page=aPage), aCurPage)
        return Res

    def Get(self, aRecords: int, aCurPage: int) -> list:
        def Loop(aBegin: int, aEnd: int):
            nonlocal Res
            for xPage in range(aBegin, aEnd + 1):
                if (xPage == aCurPage):
                    Res.append(self.ToTuple(xPage, xPage, True))
                else:
                    Res.append(self.ToTuple(xPage, xPage))

        Pages = math.ceil(aRecords / self.PerPage)
        aCurPage = max(1, min(Pages, aCurPage))
        Begin = max(1, aCurPage - self.Visible // 2)
        End = min(Pages, Begin + self.Visible - 1)

        if (End - Begin + 1 < self.Visible):
            Begin = max(1, End - self.Visible + 1)

        Res = []
        if (Pages > self.Visible + 2):
            if (Begin > 1):
                Res.append(self.ToTuple(1, 1))
                if (Begin > 2):
                    Res.append(self.ToTuple(Begin - 1, self.Back))
            Loop(Begin, End)
            if (End < Pages):
                if (End < Pages - 1):
                    Res.append(self.ToTuple(End + 1, self.Forward))
                Res.append(self.ToTuple(Pages, Pages))
        else:
            Loop(1, Pages)
        return Res
