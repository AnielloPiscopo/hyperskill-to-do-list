from django.test import TestCase
from rest_framework.throttling import AnonRateThrottle
from core.throttling import LoginRateThrottle


class LoginRateThrottleTest(TestCase):
    def test_is_subclass_of_anon_rate_throttle(self):
        self.assertTrue(issubclass(LoginRateThrottle, AnonRateThrottle))

    def test_scope_is_login(self):
        self.assertEqual(LoginRateThrottle.scope, 'login')