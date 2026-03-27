import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import generate_notification


class TestNotification(unittest.TestCase):

    def test_invalid_subscription_should_be_rejected(self):
        # Arrange
        user_data = {
            "role": "admin",
            "subscription": "free1",
            "active": True,
            "logged_in": True
        }

        # Act
        result = generate_notification(user_data)

        # Assert
        self.assertEqual(result, "Invalid subscription")

    def test_missing_subscription_should_return_invalid_data(self):
        # Arrange
        user_data = {
            "role": "admin"
        }

        # Act
        result = generate_notification(user_data)

        # Assert
        self.assertEqual(result, "Invalid notification data")

    def test_notification_should_fail_if_user_not_active(self):
        # Arrange
        user_data = {
            "role": "admin",
            "subscription": "premium",
            "active": False,
            "logged_in": True
        }

        # Act
        result = generate_notification(user_data)

        # Assert
        self.assertEqual(result, "User is not active")

    def test_notification_should_fail_if_user_not_logged_in(self):
        # Arrange
        user_data = {
            "role": "admin",
            "subscription": "premium",
            "active": True,
            "logged_in": False
        }

        # Act
        result = generate_notification(user_data)

        # Assert
        self.assertEqual(result, "User must be logged in")


if __name__ == "__main__":
    unittest.main()