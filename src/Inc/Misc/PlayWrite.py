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
from Inc.Util.Obj import Iif


async def GetUrlData(aUrl: str) -> str:
    Response = None
    async def ResponseHandler(response_obj):
        nonlocal Response
        if (response_obj.url == aUrl):
            Response = response_obj

    async with async_playwright() as PW:
        Browser = await PW.chromium.launch(headless=True)
        Page = await Browser.new_page()
        Page.on('response', ResponseHandler)
        await Page.goto(aUrl)

        # Wait for the page to load completely
        await Page.wait_for_load_state('networkidle')

        Content = await Page.content()
        await Browser.close()
        return {
            'data': Content,
            'status': Iif(Response, Response.status, -1)
        }
