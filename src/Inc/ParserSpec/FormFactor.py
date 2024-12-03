# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Common import TSpecBase

class TSpecFormFactor(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'tower': [
                r'tower',
                r'башня',
                r'корпус'
            ],
            'sff': [
                r'sff',
                r'small form factor'
            ],
            'usff': [
                r'usff',
                r'ultra small form factor'
            ],
            'desktop':[
                r'desktop',
                r'десктоп'
            ],
            'mini': [
                r'mini',
                r'tiny',
                r'міні',
                r'мини'
            ],
            'aio': [
                r'all.?in.?one',
                r'\baio\b',
                r'моноблок'
            ]
        }
        return Res

    def _OnParse(self, aMatch) -> list:
        return True
