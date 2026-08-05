from rest_framework.throttling import AnonRateThrottle

__all__ = ['LoginRateThrottle']

class LoginRateThrottle(AnonRateThrottle):
    """Rate throttle for login and register endpoints.

    Uses the 'login' scope defined in DEFAULT_THROTTLE_RATES (currently 5/minute),
    keyed by the requester's IP address since those endpoints are public.
    """

    scope = 'login'