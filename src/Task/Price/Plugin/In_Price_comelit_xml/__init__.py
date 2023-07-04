# Created: 2023.02.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://sklep.comel-it.com


import os
#
from Inc.ParserX.Common import TPluginBase
from .Main import TCategory, TProduct


class TIn_Price_comelit_xml(TPluginBase):
    async def Run(self):
        Engine = None

        Category = TCategory(self)
        if (not os.path.exists(Category.GetFile())):
            Engine = Category.InitEngine()
            Category.SetSheet('category')
        await Category.Load()

        Product = TProduct(self)
        if (not os.path.exists(Product.GetFile())):
            Product.InitEngine(Engine)
            Product.SetSheet('item')
        await Product.Load()

        return {'TDbCategory': Category.Dbl, 'TDbProductEx': Product.Dbl}
