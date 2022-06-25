"""Tests for aioschluter package."""
import json

import aiohttp
import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from schluter import (
    SchluterAPi,
    ApiError,
)

VALID_USERNAME = "valid_user@someplace.org"
INVALID_USERNAME = "invalid_user@someplace.org"
VALID_PASSWORD = "randomstring02890032"
INVALID_PASSORD = "invalidstring998908"


@pytest.mark.asyncio
async def test_valid_user():
    """Test with valid username"""
    pass


@pytest.mark.asyncio
async def test_invalid_user():
    """Test with invalid username"""
    pass


@pytest.mark.asyncio
async def test_valid_password():
    """Test with valid user and valid password"""
    pass


@pytest.mark.asyncio
async def test_invalid_password():
    """Test with valid user and invalid password"""
    pass


@pytest.mark.asyncio
async def test_get_current_thermostats():
    """Test valid current thermostat data"""
    pass
