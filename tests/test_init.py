"""Tests for aioschluter package."""
import json
from datetime import datetime

import pytest
from aiohttp import ClientSession
from aioresponses import CallbackResult, aioresponses

from aioschluter import InvalidSessionIdError, InvalidUserPasswordError, SchluterApi
from aioschluter.const import REGULATION_MODE_SCHEDULE

VALID_USERNAME = "valid_user@someplace.org"
INVALID_USERNAME = "invalid_user@someplace.org"
VALID_PASSWORD = "somevalidpassword"
INVALID_PASSWORD = "someinvalidpassword"


@pytest.mark.asyncio
async def test_valid_user():
    """Test with valid username."""
    with open("tests/fixtures/valid_user_data.json", encoding="utf-8") as file:
        logon_data = json.load(file)

    websession = ClientSession()
    sessionid = None

    with aioresponses() as session_mock:
        # pylint:disable=line-too-long
        session_mock.post(
            "https://ditra-heat-e-wifi.schluter.com/api/authenticate/user",
            payload=logon_data,
        )
        schluter = SchluterApi(websession)
        try:
            sessionid = await schluter.async_get_sessionid(
                VALID_USERNAME, VALID_PASSWORD
            )
        except InvalidUserPasswordError as ex:
            assert False, f"Raised InvalidUserPasswordError exception {ex}"

    await websession.close()
    assert sessionid == "85j7W9xNTku1bqDb4SCnPA"
    assert schluter.sessionid == "85j7W9xNTku1bqDb4SCnPA"
    assert isinstance(schluter.sessionid_timestamp, datetime)


@pytest.mark.asyncio
async def test_invalid_user():
    """Test with invalid username."""
    with open("tests/fixtures/invalid_user_data.json", encoding="utf-8") as file:
        logon_data = json.load(file)

    websession = ClientSession()
    sessionid = None

    with aioresponses() as session_mock:
        # pylint:disable=line-too-long
        session_mock.post(
            "https://ditra-heat-e-wifi.schluter.com/api/authenticate/user",
            payload=logon_data,
        )
        schluter = SchluterApi(websession)
        try:
            sessionid = await schluter.async_get_sessionid(
                INVALID_USERNAME, INVALID_PASSWORD
            )
        except InvalidUserPasswordError as ex:
            assert True, f"Raised InvalidUserPasswordError exception {ex}"

    await websession.close()
    assert schluter.sessionid is None
    assert sessionid is None


@pytest.mark.asyncio
async def test_invalid_password():
    """Test with valid user and invalid password."""
    with open("tests/fixtures/invalid_password_data.json", encoding="utf-8") as file:
        logon_data = json.load(file)

    websession = ClientSession()
    sessionid = None

    with aioresponses() as session_mock:
        # pylint:disable=line-too-long
        session_mock.post(
            "https://ditra-heat-e-wifi.schluter.com/api/authenticate/user",
            payload=logon_data,
        )
        schluter = SchluterApi(websession)
        try:
            sessionid = await schluter.async_get_sessionid(
                VALID_USERNAME, INVALID_PASSWORD
            )
        except InvalidUserPasswordError as ex:
            assert True, f"Raised InvalidUserPasswordError exception {ex}"

    await websession.close()
    assert schluter.sessionid is None
    assert sessionid is None


@pytest.mark.asyncio
async def test_get_current_thermostats():
    """Test valid current thermostat data."""
    with open("tests/fixtures/thermostats_data.json", encoding="utf-8") as file:
        thermostat_data = json.load(file)

    websession = ClientSession()
    thermostats = {}
    sessionid = "abcd12345456"

    with aioresponses() as session_mock:
        # pylint:disable=line-too-long
        session_mock.get(
            f"https://ditra-heat-e-wifi.schluter.com/api/thermostats?sessionId={sessionid}",  # noqa: E501
            payload=thermostat_data,
        )
        schluter = SchluterApi(websession)
        try:
            thermostats = await schluter.async_get_current_thermostats(sessionid)
        except InvalidSessionIdError as ex:
            assert False, f"Raised InvalidSessionIdError exception {ex}"

    await websession.close()
    assert thermostats["1084135"].name == "Bathroom"
    assert thermostats["1084135"].regulation_mode == REGULATION_MODE_SCHEDULE


def unauthorized_callback(url, **kwargs):
    """Simulate UNAUTHRIZE(401) status code."""
    # pylint: disable=unused-argument
    return CallbackResult(status=401)


@pytest.mark.asyncio
async def test_get_current_thermostats_with_wrong_sessionid():
    """Test invalid call to current thermostat data."""
    with open("tests/fixtures/thermostats_data.json", encoding="utf-8") as file:
        thermostat_data = json.load(file)

    websession = ClientSession()
    sessionid = "abcd12345456"

    with aioresponses() as session_mock:
        # pylint:disable=line-too-long
        session_mock.get(
            f"https://ditra-heat-e-wifi.schluter.com/api/thermostats?sessionId={sessionid}",  # noqa: E501
            payload=thermostat_data,
            callback=unauthorized_callback,
        )
        schluter = SchluterApi(websession)
        try:
            await schluter.async_get_current_thermostats(sessionid)
        except InvalidSessionIdError as ex:
            assert True, f"Raised InvalidSessionIdError exception {ex}"

    await websession.close()


# @pytest.mark.asyncio
# async def test_success_set_temperature():
#   """ Test setting the temerature of a specific thermostat"""
#   with open("tests/fixtures/thermostat_set_data.json", encoding="utf-8") as file:
#       success_data = json.load(file)
#
#   websession = ClientSession
#   sessionid = "abcd12345456"
#   serialnumber = "abcd12245"
#   temperature = 22.5
#
#   with aioresponses() as session_mock:
#       #pylint:disable=line-too-long
#       session_mock.post(
#           f"https://ditra-heat-e-wifi.schluter.com/api/thermostat?sessionId={sessionid}&serialnumber={serialnumber}", # noqa: E501
#           payload=success_data,
#       )
#       schluter = SchluterApi(websession)
#
#       try:
#           res = await schluter.async_set_temperature(sessionid, serialnumber, temperature) # noqa: E501
#       except InvalidSessionIdError as ex:
#           assert False, f"Raised InvalidSessionIdError exception {ex}"
#
#   await websession.close()
#   assert res is True
