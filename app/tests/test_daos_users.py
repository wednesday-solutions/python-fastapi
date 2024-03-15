from __future__ import annotations

from collections import namedtuple
from datetime import datetime
from unittest.mock import patch

import pytest
from alchemy_mock.mocking import AlchemyMagicMock
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
from freezegun import freeze_time

from app.daos.users import create_user
from app.daos.users import get_user
from app.schemas.users.users_request import CreateUser


@pytest.fixture
def mock_create_cache():
    with patch("app.wrappers.cache_wrappers.create_cache") as mock_create_cache:
        yield mock_create_cache


@pytest.fixture
def mock_retrieve_cache():
    with patch("app.wrappers.cache_wrappers.retrieve_cache") as mock_retrieve_cache:
        yield mock_retrieve_cache


@patch("app.wrappers.cache_wrappers.create_cache")
@pytest.mark.asyncio
@freeze_time("2024-01-01")
async def test_get_user(self, mock_create_cache):
    # Mocking cache functions
    mock_create_cache.return_value = None

    # Mocking the database session
    mock_db_session = AlchemyMagicMock()

    # Assuming User model is imported from your module
    User = namedtuple("User", ["id", "name", "email", "mobile", "created_at", "updated_at"])
    user = User(
        id=1,
        name="John",
        email="john@example.com",
        mobile=1234567890,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    # Mocking the query method to return the user object
    mock_db_session.query.return_value.where.return_value.with_entities.return_value.first.return_value = user

    # Call the function you want to test
    result = await get_user(1, mock_db_session)

    # Assert the result
    assert result == user


# Mock data
create_user_data = CreateUser(
    name="Test User",
    email="test@gmail.com",
    mobile="1234567890",
    password="Test@123",
)


# Mocking the database session
@pytest.fixture
def db_session():
    return UnifiedAlchemyMagicMock()


# Test if user is created successfully
def test_create_user(db_session):
    response = create_user(create_user_data, db_session)
    expected_response = {
        "success": True,
        "message": "User registered successfully.",
        "data": None,
    }
    assert response == expected_response
