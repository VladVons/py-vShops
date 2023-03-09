# Created: 2021.02.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


try:
    import asyncio
except ModuleNotFoundError:
    import uasyncio as asyncio


async def CheckHost(aHost: str, aPort: int = 80, aTimeOut: int = 1) -> bool:
    try:
        await asyncio.wait_for(asyncio.open_connection(aHost, aPort), timeout=aTimeOut)
        Res = True
    except:
        Res = False
    return Res
