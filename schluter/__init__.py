"""
Async Python wrapper to get data from schluter ditra heat thermostats via the
Schluter DITRA-HEATER-E-WIFI Api
"""

import json
import logging
from typing import Any, Dict, cast

from aiohttp import ClientSession

from .const import (
    API_APPLICATION_ID,
    API_AUTH_URL,
    API_GET_THERMOSTATS_URL,
    API_SET_TEMPERATURE_URL,
    HTTP_OK,
    HTTP_UNAUTHORIZED,
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
        self.username = username
        self.password = password
        self._session = session
        self.sessionid = None

    @staticmethod
    def _extract_thermostats_from_groups(groups: dict[str, Any]):
        for group in groups:
            _LOGGER.debug(group)
        return True
#      return {key: data[key] for key in data}

    async def async_validate_user(self):
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

    async def async_get_current_thermostats(self) -> dict[str, Any]:
        """Get the current settings for all thermostats"""
        if self.sessionid is None:
            _LOGGER.debug("Getting Schluter Api session id")
            self.sessionid = await self.async_validate_user()

        params = {"sessionId": self.sessionid}
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
        # extract the thermostat groups from data
        groups = data["Groups"]
        return self._extract_thermostats_from_groups(groups)


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
