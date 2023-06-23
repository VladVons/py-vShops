# Created: 2023.06.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
import aiohttp
from bs4 import BeautifulSoup
#
from Inc.Ean import TEan
from Inc.Util.Obj import DeepGetByList
from IncP.Log import Log
from .. import TParserBase


class TParser(TParserBase):
    UrlRoot = 'https://bscanner.com.ua'

    async def Init(self):
        Cookie = '_ga=GA1.1.905222944.1685582784; _gcl_au=1.1.1451803123.1685582785; city_id=eyJpdiI6Ijg1TjhSc1dWTTE5QXJzYmZRK0dyVFE9PSIsInZhbHVlIjoieDRvcktuSGUwUUNXdjQrTnZkK0s1Rkw2UCt3bVdLZ014bHljQytvMDB2YnExSnB6TTRhYTNUVkFzd0FpeTVVRyIsIm1hYyI6IjlkZDk2NDAyNTM2YjU2ZGM1ZDcxODI4N2Q2OWU3N2VkOTdlMmRlZjFhZjIxMDQwNzdmZWMxZTZhNTA0NTRiZTEiLCJ0YWciOiIifQ==; __cf_bm=jnyCZbb9im4RCwpTjUvQ8hROBwEhtsj6x3wNL_KLzf8-1685615388-0-Ae0wr5NMqtS5LLZp64L0Cdko4CYpN/+KD0BhRMMKr2RsnaJ0s/XL8enzU5WMryKIHdD4Akmpyf0oqT6FE9rKBBIE8sgq4ORS6l6Zpwx3lZA8; barcodes=eyJpdiI6InJPZEVnYkRRcVJPWGZsQWZxOXMwMlE9PSIsInZhbHVlIjoicTVlT1FRcEEyNkVOdkFOMTNOSjJlTHpGYmR5K0FkQzdNelI4RFdOb2tCeG9rdkswWk9pWlRCazBNeXlGOGJlOXZDdlRTNVZjOEIrSFQ3Z2duNHBrbFF6cVF4bUVzbUZLSzloQ1piSXlVWXFlL0d5NUVDNnlCTnJqUUJYMVpOZTA1cy8zUWdLSFNOTDlyQ0dHbml1TGZBPT0iLCJtYWMiOiIyY2E2Nzc0MDk0YjFkYjdiYjVlOGI2MGY3Njc0ZjYzZTNhNWY5OGY4MjJiNTFjMWNmY2YyZjkyYjQ0NjFkNWYwIiwidGFnIjoiIn0=; _ga_4BJ2Y7E7XQ=GS1.1.1685615331.3.1.1685615426.0.0.0; XSRF-TOKEN=eyJpdiI6ImFTTUJOU0dPWFNoUm9yN1Z6WjZ3c3c9PSIsInZhbHVlIjoiYjVaVTRpY25ONDhRbjBZSnhUeWRiMDJJSE9lSG1INk53Y0RHMHQxdGpDQnAzZ0QxazV0eUo2Wmp4L1RNYjJTcDJRQzQxWWdNL3ZXcG5hVUc4UHdBZTFrTlFwdUNWS1NFVDJHVGo1eTc1YXVEN0xUNmtWOHp1VjdMeXltYUZyNkMiLCJtYWMiOiJiNDllYzA5MjlmZmFkMDlhMzMwMjMxNWVmMmI0YzcwNjRiM2RmNTAzOGQ2OWZlNGYwYTNhN2ExMmU2NGY4N2IyIiwidGFnIjoiIn0=; bscanner_session=eyJpdiI6Im53NFFma2VuVDFldFVBTkFJZTN3bnc9PSIsInZhbHVlIjoiSmRlSHBlclJRSnp5YlBqNHk0cE9mMHhGemJFU2FxOG51RHB2RWtIeFRvVzFkRXRkKzIvVDh6dUZXUERzMVdKVnBtL0FSSk1oc09MdldoNTNUOEh0Zzd5UTV3dlVKN0tRRkhoWWZrMXNHanljcCtvMjMxc0xmUlk2VE4zazhnYXAiLCJtYWMiOiI2MDU5YmRkMTBmMWVkYWUzYjZlNDU0MGU3YWE5ZTYzZWZiMjI4N2EwNDI4YjllNTRmNDkwOWNlYWUxNTc0YjRjIiwidGFnIjoiIn0='
        self.Headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': Cookie

        }
        self.Token = 'vrHAfeN5TLvLjX314tbYhiBeVd2Hbq1A9Lp7Hxao'

    async def _GetData(self, aCode: str) -> dict:
        if (not self.CheckEan(aCode)):
            return

        Url = f'{self.UrlRoot}/api/search-suggestions'
        Payload = f'searchVal={aCode}&_token={self.Token}'

        async with aiohttp.ClientSession() as Session:
            async with Session.post(Url, data=Payload, headers=self.Headers) as Response:
                Data = await Response.read()
                try:
                    Data = json.loads(Data)
                except ValueError:
                    assert(False), 'import new (Cookie + Payload token) from browser. Auto parser not implemented yet'

                if (Data):
                    Product = Data[0]
                    if (aCode == Product['barcode']):
                        #Image = f"{self.UrlRoot}/storage/{Product['image']}"
                        Url = f'{self.UrlRoot}/{aCode}'
                        async with Session.get(Url) as Response:
                            Data = await Response.read()
                            ResParse = self.ParseScheme(Data)
                            Res = ResParse.get('data')
                            if (Res) and (TEan(aCode).Check()):
                                if (DeepGetByList(Res, ['features', 'main'], [''])[0] == 'Немає інформації про склад'):
                                    del Res['features']
                                Res['url'] = Url
                                return Res
