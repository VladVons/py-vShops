# Created: 2024.08.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from . import TIn_Price_pcdata_xlsx, TPriceNotebook


class TIn_Price_pcdata_xlsx_ExtDrogobich(TIn_Price_pcdata_xlsx):
    def GetHandlers(self) -> dict:
        return {
            'Laptops': {
                'parser': TPriceNotebook, 'category_id': 1, 'category': "Ноутбук"
            }
        }
