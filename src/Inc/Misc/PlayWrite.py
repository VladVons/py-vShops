# Created: 2024.09.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
#pip3 install playwrite
#playwrite install
#
#sudo apt-get install --no-install-recommends\
#  libnss3\
#  libnspr4\
#  libatk1.0-0t64\
#  libatk-bridge2.0-0t64\
#  libcups2t64\
#  libdrm2\
#  libatspi2.0-0t64\
#  libxcomposite1\
#  libxdamage1\
#  libxfixes3\
#  libxrandr2\
#  libgbm1\
#  libpango-1.0-0\
#  libcairo2\
#  libasound2t64


from playwright.async_api import async_playwright
from Inc.Var.Obj import Iif


async def UrlGetData(aUrl: str) -> str:
    async with async_playwright() as PW:
        Browser = await PW.chromium.launch(headless=True)
        Page = await Browser.new_page()
        #Page.set_default_timeout(5000)
        #Page.set_default_navigation_timeout(5000)

        Response = await Page.goto(aUrl, wait_until="domcontentloaded", timeout=5000)
        Content = await Page.content()
        await Browser.close()
        return {
            'data': Content,
            'status': Iif(Response, Response.status, -1)
        }
