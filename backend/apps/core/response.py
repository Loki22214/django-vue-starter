from typing import Any

from rest_framework import status
from rest_framework.response import Response


class APIResponse:
    """Utility class for standardized DRF API responses.

    Methods return a DRF `Response` with a consistent JSON shape used
    across the project.
    """

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
    ) -> Response:
        """Return a standard success response.

        Args:
            data: The response payload.
            message: Human-friendly message.
            status_code: HTTP status code.
        """
        payload = {
            "success": True,
            "code": status_code,
            "message": message,
            "data": data,
        }
        return Response(payload, status=status_code)

    @staticmethod
    def error(
        message: str = "Error",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        errors: dict[str, Any] | list | None = None,
    ) -> Response:
        """Return a standard error response.

        Keep `errors` flexible so validation errors can be passed through.
        """
        payload = {
            "success": False,
            "code": status_code,
            "message": message,
            "errors": errors,
        }
        return Response(payload, status=status_code)

    @staticmethod
    def paginated(
        data: Any = None,
        pagination: dict[str, Any] | None = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
    ) -> Response:
        """Return a paginated response payload.

        - `data` should be the current page's serialized items.
        - `pagination` should contain keys like `count`, `next`, `previous`,
          `page`, `page_size` or any meta the frontend expects.
        If using DRF pagination classes, prefer `paginator.get_paginated_response(...)`
        from the view; this helper is useful when you construct the pagination
        metadata yourself.
        """
        payload: dict[str, Any] = {
            "success": True,
            "code": status_code,
            "message": message,
            "data": data,
        }
        if pagination is not None:
            payload["pagination"] = pagination
        return Response(payload, status=status_code)
