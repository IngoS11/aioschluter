import asyncio
import logging

from aiohttp import ClientError, ClientSession

from aioschluter import (
    ApiError,
    InvalidUserPasswordError,
    InvalidSessionIdError,
    SchluterApi,
)

## specify the username and password that you have on the Schluter DITRA-HEATER-E-WIFI
## site at https://ditra-heat-e-wifi.schluter.com/
SCHLUTER_USERNAME = "XXXX"
SCHLUTER_PASSWORD = "XXXX"

logging.basicConfig(level=logging.DEBUG)


async def main():
    async with ClientSession() as websession:
        try:
            schluter = SchluterApi(websession)

            sessionid = await schluter.async_get_sessionid(
                SCHLUTER_USERNAME, SCHLUTER_PASSWORD
            )
            thermostats = await schluter.async_get_current_thermostats(sessionid)
        except (
            ApiError,
            ClientError,
            InvalidUserPasswordError,
            InvalidSessionIdError,
        ) as error:
            print(f"Error: {error}")
        else:
            for thermostat in thermostats.values():
                print(thermostat)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
