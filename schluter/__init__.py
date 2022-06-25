"""
Async Python wrapper to get data from schluter ditra heat thermostats via the
Schluter DITRA-HEATER-E-WIFI Api
"""

import json
import logging
from typing import Any, Dict, cast

from aiohttp import ClientSession

from .const import (
    API_AUTH_URL,
    API_GET_THERMOSTATS_URL,
    API_SET_TEMPERATURE_URL,
    API_APPLICATION_ID,
    HTTP_UNAUTHORIZED,
    HTTP_OK,
)

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
        self._username = username
        self._password = password
        self._session = session
        self._sessionid = None

    async def async_validate_user(self):
        """Validate the username and password for the Schluter API"""
        async with self._session.post(
            API_AUTH_URL,
            json={
                "Email": self._username,
                "Password": self._password,
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

        self._sessionid = data["SessionId"]
        return self._sessionid

    async def async_get_current_thermostats(self) -> dict[str, Any]:
        """Get the current settings for all thermostats"""
        if self._sessionid is None:
            _LOGGER.debug("Getting Schluter Api session id")
            self._sessionid = await self.async_validate_user()

        params = {"sessionId": self._sessionid}
        async with self._session.get(API_GET_THERMOSTATS_URL, params=params) as resp:
            if resp.status == HTTP_UNAUTHORIZED:
                raise InvalidUserPasswordError(
                    f"Invalid session id supplied when calling Schluter Api : {resp.status}"
                )
            if resp.status != HTTP_OK:
                raise ApiError(f"Invalid Response from Schluter Api: {resp.status}")

            _LOGGER.debug(
                "Data retrieved from %s, status: %s",
                API_GET_THERMOSTATS_URL,
                resp.status,
            )
            data = await resp.json()
        _LOGGER.debug("Stop")
        groups = data["Groups"]["Thermostats"]
        return {key: groups[key] for key in groups}


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