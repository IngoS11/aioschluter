"""Tests for aioschluter package."""
import json

import aiohttp
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

    websession = aiohttp.ClientSession()
    sessionid = None

    with aioresponses() as session_mock:
        # pylint:disable=line-too-long
        session_mock.post(
            "https://ditra-heat-e-wifi.schluter.com/api/authenticate/user",
            payload=logon_data,
        )
        schluter = SchluterApi(VALID_USERNAME, VALID_PASSWORD, websession)
        try:
            sessionid = await schluter.async_validate_user()
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

    websession = aiohttp.ClientSession()
    sessionid = None

    with aioresponses() as session_mock:
        # pylint:disable=line-too-long
        session_mock.post(
            "https://ditra-heat-e-wifi.schluter.com/api/authenticate/user",
            payload=logon_data,
        )
        schluter = SchluterApi(INVALID_USERNAME, INVALID_PASSWORD, websession)
        try:
            sessionid = await schluter.async_validate_user()
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

    websession = aiohttp.ClientSession()
    sessionid = None

    with aioresponses() as session_mock:
        # pylint:disable=line-too-long
        session_mock.post(
            "https://ditra-heat-e-wifi.schluter.com/api/authenticate/user",
            payload=logon_data,
        )
        schluter = SchluterApi(VALID_USERNAME, INVALID_PASSWORD, websession)
        try:
            sessionid = await schluter.async_validate_user()
        except InvalidUserPasswordError as ex:
            assert True, f"Raised InvalidUserPasswordError exception {ex}"

    await websession.close()
    assert schluter.sessionid is None
    assert sessionid is None


@pytest.mark.asyncio
async def test_get_current_thermostats():
    """Test valid current thermostat data"""
    pass
