# Created: 2022.03.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ..Session import Session
from .FormBase import TFormBase


class TForm(TFormBase):
    def _DoInit(self):
        self.out.title = 'Index'
        self.Pages = {
            '/form/soup_help': 'soup help',
            '/form/soup_get': 'soup get',
            '/form/soup_make': 'soup make',
            '/form/soup_test': 'soup test',
            '/form/sites_list': 'sites list',
            '/form/sites_add': 'sites_add',
            '/form/tools': 'tools',
        }

    async def _Render(self):
        self.out.data.pages = {
            Key: Val
            for Key, Val in self.Pages.items()
            if (Session.CheckUserAccess(Key))
        }
