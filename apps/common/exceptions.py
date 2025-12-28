from rest_framework.exceptions import APIException
from rest_framework import status

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'

class Conflict(APIException):
    status_code = 409
    default_detail = 'Resource state conflict.'
    default_code = 'conflict'
