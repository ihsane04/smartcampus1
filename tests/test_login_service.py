import unittest

from src.login_service import LoginService, MSG_INVALID, MSG_SUCCESS


class LoginServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = LoginService()
        self.service.register("student@ensak.ma", "secret123")

    def test_login_with_correct_credentials(self):
        ok, message = self.service.login("student@ensak.ma", "secret123")
        self.assertTrue(ok)
        self.assertEqual(message, MSG_SUCCESS)

    def test_wrong_password_returns_clear_message(self):
        ok, message = self.service.login("student@ensak.ma", "mauvais")
        self.assertFalse(ok)
        self.assertEqual(message, MSG_INVALID)

    def test_unknown_email_is_rejected(self):
        ok, _ = self.service.login("inconnu@ensak.ma", "secret123")
        self.assertFalse(ok)

    def test_inactive_account_is_rejected(self):
        self.service.register("ancien@ensak.ma", "pwd", active=False)
        ok, _ = self.service.login("ancien@ensak.ma", "pwd")
        self.assertFalse(ok)

    def test_three_failures_are_logged(self):
        with self.assertLogs("smartcampus.security", level="WARNING"):
            for _ in range(3):
                self.service.login("student@ensak.ma", "mauvais")


if __name__ == "__main__":
    unittest.main()