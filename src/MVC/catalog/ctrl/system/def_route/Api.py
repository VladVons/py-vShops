# Created: 2024.02.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Main(self, aData: dict) -> dict:
    Msg = f'Route {aData.get("route")} handled by {__package__}'
    print(Msg)
