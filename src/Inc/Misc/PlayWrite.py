# Created: 2024.09.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# pip3 install playwrite
# playwrite install chromium
#
# sudo apt-get install --no-install-recommends\
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


import asyncio
import tracemalloc
from playwright.async_api import async_playwright
from Inc.Var.Obj import Iif


tracemalloc.start()

async def UrlGetData(aUrl: str, aWaitFor: str = None) -> str:
    ContextOpt = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "locale": "uk-UA",
        "extra_http_headers": {
            "Accept-Language": "uk-UA"
        }
    }

    async with async_playwright() as PW:
        async with await PW.chromium.launch(headless=True) as Browser:
            Context = await Browser.new_context(**ContextOpt)
            #Page = await Browser.new_page()
            Page = await Context.new_page()

            #Response = await Page.goto(aUrl, wait_until="load", timeout=10000)
            Response = await Page.goto(aUrl, wait_until="domcontentloaded", timeout=10000)
            await asyncio.sleep(1)
            if (aWaitFor):
                #aWaitFor = 'ul[class="pagination"]'
                await Page.wait_for_selector(aWaitFor, timeout=3000)
            Content = await Page.content()

        return {
            'data': Content,
            'status': Iif(Response, Response.status, -1)
        }
