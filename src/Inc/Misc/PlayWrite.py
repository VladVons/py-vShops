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

import tracemalloc
from playwright.async_api import async_playwright
from Inc.Var.Obj import Iif


tracemalloc.start()

async def UrlGetData(aUrl: str, aWaitFor: str = None) -> str:
    ContextOpt = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "viewport": {"width": 1280, "height": 720},
        "permissions": ["geolocation"],
        "locale": "fr-FR",
        "extra_http_headers": {
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    }

    async with async_playwright() as PW:
        async with await PW.chromium.launch(headless=True) as Browser:
            Page = await Browser.new_page()
            #await Browser.new_context(**ContextOpt)
            Response = await Page.goto(aUrl, wait_until="domcontentloaded", timeout=10000)
            if (aWaitFor):
                #aWaitFor = 'ul[class="pagination"]'
                await Page.wait_for_selector(aWaitFor, timeout=3000)
            Content = await Page.content()

        return {
            'data': Content,
            'status': Iif(Response, Response.status, -1)
        }
