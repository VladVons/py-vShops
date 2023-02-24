# Created: 2022.03.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from .FormBase import TFormBase

class TForm(TFormBase):
    def _DoInit(self):
        self.out.title = 'Information'
