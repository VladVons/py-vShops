# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from ._Common import TSpecBase

class TSpecStorage(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'storage': [
                # 256 ssd | 512 hdd
                r'(\d{3,4})\s*(ssd|hdd|nvme|m2|m\.2|sas)',

                # 512Gb | 2048 gb | 256gb-ssd
                r'(\d{3,4})\s*(gb|гб)\s*-?(ssd|hdd|nvme|m2|m\.2|sas)?',

                # 2tb | 12 tb
                r'(\d{1,2})\s*(tb|тб)\s*-?(ssd|hdd|nvme|m2|m\.2|sas)?'
            ]
        }
        return Res
