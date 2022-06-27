# Schluter API Python wrapper
An async Python wrapper for the [Schluter-DITRA-E-WIFI](https://www.schluter.com/schluter-us/en_US/ditra-heat-wifi) Wi-Fi Themostat

## User
Create a user for your thermostats at [https://ditra-heat-e-wifi.schluter.com/](https://ditra-heat-e-wifi.schluter.com/)

## Basic Example
```python
import asyncio
import logging

from aiohttp import ClientError, ClientSession

from aioschluter import ApiError, InvalidUserPasswordError, SchluterApi

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
            # Login to the Schluter API to get a session id
            sessionid = await schluter.async_login()
            # Retreive your currently configured thermostats
            thermostats = await schluter.async_get_current_thermostats(sessionid)
        except (
            ApiError,
            ClientError,
            InvalidUserPasswordError,
        ) as error:
            print(f"Error: {error}")
        else:
            for thermostat in thermostats.values():
                print(thermostat)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```