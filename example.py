import asyncio
import logging

from aiohttp import ClientError, ClientSession
from schluter import ApiError, SchluterApi, InvalidUserPasswordError

## specify the username and password that you have on the Schluter DITRA-HEATER-E-WIFI
## site at https://ditra-heat-e-wifi.schluter.com/
SCHLUTER_USERNAME = 'XXXX'
SCHLUTER_PASSWORD = 'XXXX'

logging.basicConfig(level=logging.DEBUG)

async def main():
    async with ClientSession() as websession:
        try:
            schluter = SchluterApi(
                SCHLUTER_USERNAME,
                SCHLUTER_PASSWORD,
                websession
            )
            thermostats = await schluter.async_get_current_thermostats()
        except (
            ApiError,
            ClientError,
            InvalidUserPasswordError,
        ) as error:
            print(f"Error: {error}")
        else:
            print(f"Thermostats: {thermostats}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
