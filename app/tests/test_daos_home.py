from __future__ import annotations

import unittest
from unittest.mock import patch

from app.daos.home import external_service_call
from app.exceptions import ExternalServiceException


class TestExternalServiceCall(unittest.TestCase):
    @patch("app.daos.home.random")
    @patch("app.daos.home.asyncio.sleep")
    async def test_external_service_call_success(self, mock_sleep, mock_random):
        # Mocking the random delay
        mock_random.uniform.return_value = 0.5  # Mocking a fixed delay for simplicity

        # Call the function
        result = await external_service_call()

        # Assertions
        mock_sleep.assert_called_once_with(0.5)  # Check if sleep is called with the correct delay
        self.assertEqual(result, "Success from external service")

    @patch("app.daos.home.random")
    @patch("app.daos.home.asyncio.sleep")
    async def test_external_service_call_failure(self, mock_sleep, mock_random):
        # Mocking the random delay
        mock_random.uniform.return_value = 0.5  # Mocking a fixed delay for simplicity
        # Mocking random.random to always trigger failure
        mock_random.random.return_value = 0.1  # Mocking a value lower than 0.2 for failure

        # Call the function and expect an exception
        with self.assertRaises(ExternalServiceException):
            await external_service_call()

        # Assertions
        mock_sleep.assert_called_once_with(0.5)  # Check if sleep is called with the correct delay


if __name__ == "__main__":
    unittest.main()
