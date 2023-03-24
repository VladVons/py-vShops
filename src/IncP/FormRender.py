# Created: 2023.03.22
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import cProfile
import pstats
from IncP.FormBase import TFormBase


class TFormRender(TFormBase):
    async def _DoRender(self):
        with cProfile.Profile() as F:
            Data = await self.ExecCtrlDef()

        Stats = pstats.Stats(F)
        Stats.sort_stats(pstats.SortKey.TIME)
        #Stats.print_stats()
        Stats.dump_stats('ExecCtrlDef.prof')

        for Key, Val in Data.get('modules', {}).items():
            if ('err' not in Val):
                pass
        self.out.modules = {'inc_right': ['one', 'two', 'three']}
