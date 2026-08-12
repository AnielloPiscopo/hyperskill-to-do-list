from drf_spectacular.utils import OpenApiResponse

RESPONSE_400 = OpenApiResponse(description='Bad request — invalid data.')
RESPONSE_401 = OpenApiResponse(description='Authentication credentials were not provided.')
RESPONSE_403 = OpenApiResponse(description='Not authorized or not authenticated.')
RESPONSE_429 = OpenApiResponse(description='Too many requests — rate limit exceeded.')