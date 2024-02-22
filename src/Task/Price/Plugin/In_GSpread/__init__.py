# Created: 2024.02.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#import gspread
#
from Inc.Misc.Request import DownloadFile
from Inc.ParserX.Common import TPluginBase


class TIn_GSpread(TPluginBase):
    # def GDownloadXlsx(self, aUrl: str, aFile: str) -> bool:
    #     AuthFile = os.path.expanduser('~/.config/gspread/service_account.json')
    #     assert(os.path.isfile(AuthFile)), f'File does not exist {AuthFile}'

    #     GSA = gspread.service_account()
    #     SH = GSA.open_by_url(aUrl)
    #     Data = SH.export(format = gspread.utils.ExportFormat.EXCEL)
    #     with open(aFile, 'wb') as F:
    #         F.write(Data)
    #         return True

    async def GDownloadXlsx(self, aUrl: str, aFile: str):
        Url = f'{aUrl}/export?format=xlsx'
        Status = await DownloadFile(Url, aFile)
        assert(Status == 200), f'Cant download {aUrl}'

    async def Run(self):
        File = self.GetFile()
        await self.GDownloadXlsx(self.Conf.GetKey('url'), File)
