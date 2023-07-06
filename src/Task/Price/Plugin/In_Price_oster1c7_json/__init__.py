# Created: 2023.07.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import json
import os
#
from Inc.ParserX.Common import TPluginBase
from .Main import TCategory, TProduct


class TIn_Price_oster1c7_json(TPluginBase):
    async def Run(self):
        File = self.GetFile()
        with open(File, 'r', encoding='cp1251') as F:
            Data = json.load(F)
        return {'TDbCategory': Category.Dbl, 'TDbProductEx': Product.Dbl}
