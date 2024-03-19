from __future__ import annotations

import json
import unittest
from collections import namedtuple
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from alchemy_mock.mocking import AlchemyMagicMock
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
from fastapi import HTTPException
from freezegun import freeze_time
from sqlalchemy import Select
from werkzeug.security import generate_password_hash

from app.daos.users import create_user
from app.daos.users import get_user
from app.daos.users import list_users
from app.daos.users import login
from app.schemas.users.users_request import CreateUser
from app.schemas.users.users_request import Login


@pytest.fixture
def mock_create_cache():
    with patch("app.wrappers.cache_wrappers.CacheUtils.create_cache") as mock_create_cache:
        yield mock_create_cache


@pytest.fixture
def mock_retrieve_cache():
    with patch("app.wrappers.cache_wrappers.CacheUtils.retrieve_cache") as mock_retrieve_cache:
        yield mock_retrieve_cache


@patch("app.wrappers.cache_wrappers.CacheUtils.create_cache")
@pytest.mark.asyncio
@freeze_time(datetime(2024, 3, 15, 17, 20, 37, 495390).strftime("%Y-%m-%d %H:%M:%S.%f"))
async def test_get_user(self, mock_create_cache):
    # Mocking cache functions
    mock_create_cache.return_value = None

    # Mocking the database session
    mock_db_session = AlchemyMagicMock()

    # Assuming User model is imported from your module
    User = namedtuple("User", ["id", "name", "email", "mobile", "created_at", "updated_at"])
    user = User(
        id=100,
        name="John",
        email="john@example.com",
        mobile=1234567890,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
    )
    # Mocking the query method to return the user object
    mock_db_session.query.return_value.where.return_value.with_entities.return_value.first.return_value = user

    # Call the function you want to test
    result = await get_user(100, mock_db_session)
    print(result)
    print(user._asdict())
    # Assert the result
    assert result == json.loads(json.dumps(user._asdict(), default=str))


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


class TestListUsers(unittest.TestCase):
    @patch("app.models.users.User")  # Patch the User model
    @patch("app.daos.users.paginate")  # Patch the paginate function
    def test_list_users_success(self, mock_paginate, mock_user):
        # Mocking the Session
        mock_session = AlchemyMagicMock()

        # Creating mock users
        user1 = UnifiedAlchemyMagicMock(id=1, name="User1", email="user1@example.com", mobile="1234567890")
        user2 = UnifiedAlchemyMagicMock(id=2, name="User2", email="user2@example.com", mobile="9876543210")

        # Mocking the query result
        mock_query = Select()

        mock_user.query = mock_query

        # Mocking the paginate function
        mock_paginate.return_value = [user1, user2]  # Assuming paginate returns the same users for simplicity

        # Call the function
        result = list_users(mock_session)

        # Assertions
        self.assertEqual(result, [user1, user2])

    @patch("app.daos.users.paginate")
    def test_list_users_exception(self, mock_paginate):
        # Mocking the Session
        mock_session = UnifiedAlchemyMagicMock()

        # Mocking the query result
        mock_query = AlchemyMagicMock()
        mock_query.all.side_effect = Exception("Test exception")

        # Mocking the User model
        mock_user = UnifiedAlchemyMagicMock()
        mock_user.query = mock_query

        # Mocking the paginate function
        mock_paginate.side_effect = HTTPException(status_code=400, detail="Test exception")

        # Call the function
        with self.assertRaises(HTTPException) as cm:
            list_users(mock_session)

        # Assertions
        self.assertEqual(cm.exception.status_code, 400)


class TestGetUser(unittest.IsolatedAsyncioTestCase):
    @patch("app.wrappers.cache_wrappers.CacheUtils.retrieve_cache")
    async def test_get_user_no_cache_no_user_found(self, mock_retrieve_cache):
        # Mocking retrieve_cache to return no cached user
        mock_retrieve_cache.return_value = None, None

        # Mocking the database session and query result
        mock_session = AlchemyMagicMock()
        mock_query = MagicMock()
        mock_query.where.return_value = mock_query
        mock_query.with_entities.return_value = mock_query
        mock_query.first.return_value = None  # Simulate no user found in the database

        mock_session.query.return_value = mock_query

        # Call the function and expect an exception
        with self.assertRaises(HTTPException) as cm:
            await get_user(0, mock_session)
        # Assertions
        mock_retrieve_cache.assert_called_once_with("user_0")
        mock_query.where.assert_called_once()
        self.assertEqual(cm.exception.status_code, 400)
        self.assertEqual(str(cm.exception.detail), "No User found for given ID.")

    # Write similar tests for other scenarios (e.g., cache hit, database query exception, cache creation exception)


login_data = Login(email="test@gmail.com", password="Test@123")


# Test if user login is successful
@patch("app.constants.jwt_utils.create_access_token")
@patch("app.daos.users.check_password_hash")
def test_login_successful(mock_create_access_token, mock_check_password_hash):
    mock_create_access_token.return_value = True
    mock_check_password_hash.return_value = True

    mock_db_session = AlchemyMagicMock()
    User = namedtuple("User", ["id", "email", "password"])
    user = User(id=1, email="test@gmail.com", password=generate_password_hash("Test@123", method="pbkdf2"))
    mock_db_session.query.return_value.where.return_value.first.return_value = user

    response = login(login_data, mock_db_session)
    expected_response = {
        "success": True,
        "message": "User logged in successfully.",
        "data": {"token": True},
    }
    assert response == expected_response


def test_login_invalid_password():
    mock_db_session = AlchemyMagicMock()

    User = namedtuple("User", ["id", "email", "password"])
    user = User(id=1, email="test@gmail.com", password="Test@13")

    mock_db_session.query.return_value.where.return_value.first.return_value = user

    with pytest.raises(Exception):
        login(login_data, mock_db_session)


if __name__ == "__main__":
    unittest.main()
