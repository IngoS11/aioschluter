"""Tests for aioschluter package."""
import json

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from schluter import InvalidUserPasswordError, SchluterApi

VALID_USERNAME = "valid_user@someplace.org"
INVALID_USERNAME = "invalid_user@someplace.org"
VALID_PASSWORD = "somevalidpassword"
INVALID_PASSWORD = "someinvalidpassword"


@pytest.mark.asyncio
async def test_valid_user():
    """Test with valid username"""
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
        schluter = SchluterApi(VALID_USERNAME, VALID_PASSWORD, websession)
        try:
            sessionid = await schluter.async_login()
        except InvalidUserPasswordError as ex:
            assert False, f"Raised InvalidUserPasswordError exception {ex}"

    await websession.close()
    assert sessionid == "85j7W9xNTku1bqDb4SCnPA"
    assert schluter.sessionid == "85j7W9xNTku1bqDb4SCnPA"


@pytest.mark.asyncio
async def test_invalid_user():
    """Test with invalid username"""
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
        schluter = SchluterApi(INVALID_USERNAME, INVALID_PASSWORD, websession)
        try:
            sessionid = await schluter.async_login()
        except InvalidUserPasswordError as ex:
            assert True, f"Raised InvalidUserPasswordError exception {ex}"

    await websession.close()
    assert schluter.sessionid is None
    assert sessionid is None


@pytest.mark.asyncio
async def test_invalid_password():
    """Test with valid user and invalid password"""
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
        schluter = SchluterApi(VALID_USERNAME, INVALID_PASSWORD, websession)
        try:
            sessionid = await schluter.async_login()
        except InvalidUserPasswordError as ex:
            assert True, f"Raised InvalidUserPasswordError exception {ex}"

    await websession.close()
    assert schluter.sessionid is None
    assert sessionid is None


@pytest.mark.asyncio
async def test_get_current_thermostats():
    """Test valid current thermostat data"""
    with open("tests/fixtures/thermostats_data.json", encoding="utf-8") as file:
        thermostat_data = json.load(file)

    websession = ClientSession()
    thermostats = {}

    with aioresponses() as session_mock:
        # pylint:disable=line-too-long
        session_mock.get(
            "https://ditra-heat-e-wifi.schluter.com/api/thermostats?sessionId=abcd12345456",
            payload=thermostat_data,
        )
        schluter = SchluterApi(VALID_USERNAME, VALID_PASSWORD, websession)
        sessionid = "abcd12345456"
        try:
            thermostats = await schluter.async_get_current_thermostats(sessionid)
        except InvalidUserPasswordError as ex:
            assert False, f"Raised InvalidUserPasswordError exception {ex}"

    await websession.close()
    assert thermostats["1084135"].name == "Bathroom"
