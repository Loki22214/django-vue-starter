from rest_framework.views import exception_handler

from .response import APIResponse


def custom_exception_handler(exc, context):
    """
    Custom exception handler that wraps the default DRF exception handler and returns standardized API responses.
    """

    response = exception_handler(exc, context)

    if response is not None:
        return APIResponse.error(
            message="Request failed",
            status_code=response.status_code,
            errors=response.data,
        )

    return APIResponse.error(message="Server Error", status_code=500, errors=None)
