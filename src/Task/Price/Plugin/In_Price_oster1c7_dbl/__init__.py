# Created: 2023.07.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import json
import os
#
from Inc.ParserX.Common import TPluginBase
from .Main import TCategory, TProduct


class TIn_Price_oster1c7_dbl(TPluginBase):
    async def Run(self):
        Category = TCategory(self)
        Engine = Category.InitEngine()
        Category.SetSheet('category')
        await Category.Load()

        Product = TProduct(self)
        Product.InitEngine(Engine)
        Product.SetSheet('product')
        await Product.Load()

        return {'TDbCategory': Category.Dbl, 'TDbProductEx': Product.Dbl}
