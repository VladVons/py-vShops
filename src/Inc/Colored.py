# Created: 2022.04.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# import Inc.Colored as Cl
# Cl.Print('Hello World colored example', Cl.cYellow)
# print(Cl.Format('World', Cl.cBlue))
# print(Cl.fg(Cl.cRed) + 'Hello ' + Cl.fg(Cl.cGreen) + 'World !')


cRed = (255, 0, 0)
cGreen = (0, 255, 0)
cBlue = (0, 0, 255)
cYellow = (255, 255, 0)
cLime = (0, 255, 0)
cCyan = (0, 255, 255)
cMagenta = (255, 0, 255)
cGray = (128, 128, 128)
cSilver = (192, 192, 192)
cWhite = (255, 255, 255)
cDef = cSilver
#

def fg(aColor: tuple) -> str:
    return '\033[38;2;%sm' % (';'.join(str(x) for x in aColor))

def Format(aText: str, aColor: tuple = cWhite) -> str:
    return fg(aColor) + aText

def Print(aText: str, aColor: tuple = cWhite):
    print(fg(aColor) + aText + fg(cDef))
