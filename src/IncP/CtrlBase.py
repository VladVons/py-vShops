# Created: 2023.03.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Loader.Lang import TLoaderLangFs
from Task.SrvCtrl.Api import TApiCtrl


class TCtrlBase():
    def __init__(self):
        self.ApiCtrl: TApiCtrl
        self.Lang = TLoaderLangFs('ua', 'MVC/lang')

    async def ExecModel(self, aMethod: str, aData: dict) -> dict:
        return await self.ApiCtrl.Loader['model'].Get(aMethod, aData)
