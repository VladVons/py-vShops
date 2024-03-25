# opencart 

import aiohttp
import asyncio

async def fetch_osm_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def get_osm_regions():
    url = "https://nominatim.openstreetmap.org/search?country=Ukraine&format=json&polygon=1&addressdetails=1"
    data = await fetch_osm_data(url)
    regions = []
    for item in data:
        if 'address' in item:
            region = item['address'].get('state', None)
            if region and region not in regions:
                regions.append(region)
    return regions

async def main():
    regions = await get_osm_regions()
    print("Список областей України з OSM:")
    for region in regions:
        print(region)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
