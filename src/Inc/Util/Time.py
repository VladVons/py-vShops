# Created: 2020.02.27
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time


# def TimeInRange(aStart, aEnd, aX):
#     if (aStart <= aEnd):
#         return (aStart <= aX <= aEnd)
#     else:
#         return (aStart <= aX) or (aX <= aEnd)

# def DTimeIt(aFunc: callable):
#     def Wrapper(*aArgs, **aK):
#         TimeStart = time.time()
#         Res = aFunc(*aArgs, **aK)
#         print(f'time: {time.time() - TimeStart:.3f}')
#         return Res
#     return Wrapper

# def DATimeIt(aFunc: callable):
#     async def Wrapper(*aArgs, **aK):
#         TimeStart = time.time()
#         Res = await aFunc(*aArgs, **aK)
#         print(f'time: {time.time() - TimeStart:.3f}')
#         return Res
#     return Wrapper

def GetDate() -> str:
    lt = time.localtime(time.time())
    R = '%d-%02d-%02d' % (lt[0], lt[1], lt[2])
    return R

def GetTime() -> str:
    lt = time.localtime(time.time())
    R = '%02d:%02d:%02d' % (lt[3], lt[4], lt[5])
    return R
