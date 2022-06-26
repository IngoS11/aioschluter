"""
Async Python wrapper to get data from schluter ditra heat thermostats via the
Schluter DITRA-HEATER-E-WIFI Api
"""

import logging
from typing import Any

from aiohttp import ClientSession

from .const import (
    API_APPLICATION_ID,
    API_AUTH_URL,
    API_GET_THERMOSTATS_URL,
    API_SET_TEMPERATURE_URL,
    HTTP_OK,
    HTTP_UNAUTHORIZED,
)
from .thermostat import Thermostat

_LOGGER = logging.getLogger(__name__)


class SchluterApi:
    """Main class to perform Schluter API requests"""

    def __init__(
        self,
        username: str,
        password: str,
        session: ClientSession,
    ):
        """Initialize."""
        self.username = username
        self.password = password
        self._session = session
        self.sessionid = None

    @staticmethod
    def _extract_thermostats_from_data(data: dict[str, Any]) -> dict[str, Any]:
        thermostats = {}
        for group in data["Groups"]:
            for tdata in group["Thermostats"]:
                thermostats[tdata["SerialNumber"]] = Thermostat(tdata)
        return thermostats

    async def async_login(self):
        """Validate the username and password for the Schluter API"""
        async with self._session.post(
            API_AUTH_URL,
            json={
                "Email": self.username,
                "Password": self.password,
                "Application": API_APPLICATION_ID,
            },
        ) as resp:
            if resp.status == HTTP_UNAUTHORIZED:
                raise InvalidUserPasswordError("Invalid username or password")
            if resp.status != HTTP_OK:
                raise ApiError(f"Invalid Response from Schluter API: {resp.status}")

            _LOGGER.debug(
                "Data retrieved from %s, status: %s", API_AUTH_URL, resp.status
            )
            data = await resp.json()

        if data["SessionId"] == "":
            if data["ErrorCode"] == 1 or data["ErrorCode"] == 2:
                raise InvalidUserPasswordError("Invalid username or password")
            _LOGGER.error(
                "Unkonwn ErrorCode was returned by Schluter API: %i",
                data["ErrorCode"],
            )
            raise ApiError("Unknown ErrorCode was returned by Schluter Api")

        self.sessionid = data["SessionId"]
        return self.sessionid

    async def async_get_current_thermostats(self, sessionid) -> dict[str, Any]:
        """Get the current settings for all thermostats"""
        if len(sessionid) == 0:
            raise InvalidSessionIdError("Invalid Session Id")

        self.sessionid = sessionid
        params = {"sessionId": sessionid}
        async with self._session.get(API_GET_THERMOSTATS_URL, params=params) as resp:
            if resp.status == HTTP_UNAUTHORIZED:
                raise InvalidUserPasswordError(
                    f"Invalid session id supplied: {resp.status}"
                )
            if resp.status != HTTP_OK:
                raise ApiError(f"Invalid Response: {resp.status}")

            _LOGGER.debug(
                "Data retrieved from %s, status: %s",
                API_GET_THERMOSTATS_URL,
                resp.status,
            )
            data = await resp.json()
        return self._extract_thermostats_from_data(data)

    async def async_set_temperature(self, sessionid, serialnumber, temperature) -> bool:
        """Set the temperature for a thermostat"""
        if len(sessionid) == 0:
            raise InvalidSessionIdError("Invalid Session Id")

        self.sessionid = sessionid
        adjusted_temp = int(temperature * 100)
        params = {"sessionId": sessionid, "serialnumber": serialnumber}

        async with self._session.post(
            API_SET_TEMPERATURE_URL,
            params=params,
            json={
                "ManualTemperature": adjusted_temp,
                "RegulationMode": 3,
                "VacationEnabled": False,
            },
        ) as resp:
            if resp.status == HTTP_UNAUTHORIZED:
                raise InvalidUserPasswordError("Invalid username or password")
            if resp.status != HTTP_OK:
                raise ApiError(f"Invalid Response from Schluter API: {resp.status}")

            _LOGGER.debug(
                "Temperature set via %s, status: %s",
                API_SET_TEMPERATURE_URL,
                resp.status,
            )
            data = await resp.json()
        return data["Success"]


class ApiError(Exception):
    """Raised when Schluter API request ended in error"""

    def __init__(self, status) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status


class InvalidUserPasswordError(Exception):
    """Raise when Username is incorrect"""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status


class InvalidSessionIdError(Exception):
    """Raise when the Schluter Session Id is missing"""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status
