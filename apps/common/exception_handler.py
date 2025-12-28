from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """
    Custom exception handler that wraps the default DRF response
    into a standardized format.
    """
    response = drf_exception_handler(exc, context)

    if response is not None:
        # Standardize error response
        custom_data = {
            "success": False,
            "error": {
                "status_code": response.status_code,
                "type": exc.__class__.__name__,
                "detail": response.data
            }
        }
        response.data = custom_data

    return response
