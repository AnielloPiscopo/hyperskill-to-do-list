from rest_framework.throttling import AnonRateThrottle

__all__ = ['LoginRateThrottle']

class LoginRateThrottle(AnonRateThrottle):
    scope = 'login'