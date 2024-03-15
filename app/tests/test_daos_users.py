from unittest.mock import MagicMock, patch
from ..daos.users import get_user
from app.models import User
import pytest
@pytest.fixture
def mock_create_cache():
    with patch('app.wrappers.cache_wrappers.create_cache') as mock_create_cache:
        yield mock_create_cache
@pytest.fixture
def mock_retrieve_cache():
    with patch('app.wrappers.cache_wrappers.retrieve_cache') as mock_retrieve_cache:
        yield mock_retrieve_cache
@patch('app.wrappers.cache_wrappers.retrieve_cache')
@patch('app.wrappers.cache_wrappers.create_cache')
async def test_get_user(self, mock_create_cache, mock_retrieve_cache):
        # Mocking cache functions
        mock_retrieve_cache.return_value = ('{"id": 1, "name": "John"}', True)
        mock_create_cache.return_value = None

        # Mocking the database session
        mock_db_session = MagicMock()

        # Assuming User model is imported from your module
        user = User(
            id=1,
            name="John",
            email="john@example.com",
            mobile="1234567890"
        )

        # Mocking the query method to return the user object
        mock_db_session.query.return_value.where.return_value.with_entities.return_value.first.return_value = user

        # Call the function you want to test
        result =   await  get_user(1, mock_db_session)
        print(result)
        # Assert the result
        self.assertEqual(result, {
            'id': 1,
            'name': 'John',
            'email': 'john@example.com',
            'mobile': '1234567890',
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'deleted_at': None
        })

        # Assert that cache functions were called
        mock_retrieve_cache.assert_called_once_with('user_1')
        mock_create_cache.assert_called_once_with('{"id": 1, "name": "John"}', 'user_1', 60)
