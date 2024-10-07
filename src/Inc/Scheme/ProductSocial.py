# Created: 2024.10.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from bs4 import BeautifulSoup


class TProductOg():
    def __init__(self, aSoup: BeautifulSoup):
        self.Root = aSoup
        self.Soup = aSoup.find('head')

    def Parse(self) -> dict:
        if (self.Soup):
            Data = {
                'og:description': self.Descr(),
                'og:image': self.Image()
            }
            return Data

    def Descr(self) -> str:
        Soup = self.Soup.find('meta', property='og:description')
        if (Soup):
            return Soup.get('content')

    def Image(self) -> str:
        Soup = self.Soup.find('meta', property='og:image')
        if (Soup):
            return Soup.get('content')
