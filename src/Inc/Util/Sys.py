# Created: 2024.10.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sys

def IsDebug():
    return any('pydevd' in str(frame) or 'pdb' in str(frame) for frame in sys._current_frames().values())
