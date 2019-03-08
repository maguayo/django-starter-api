from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from project.functions import response_wrapper
from rest_framework.exceptions import (
    ValidationError,
    NotFound,
    NotAuthenticated,
)
from django.http import Http404


def custom_exception_handler(exc, context):  # type: ignore
    """
    Custom exception handler for rest api views
    """

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        return Response(
            response_wrapper(
                data=response.data, success=False, code=response.status_code
            ),
            status=response.status_code,
        )

    if isinstance(exc, NotAuthenticated):
        return Response(
            response_wrapper(
                data=response.data, success=False, code=response.status_code
            ),
            status=response.status_code,
        )

    if (
        isinstance(exc, ObjectDoesNotExist)
        or isinstance(exc, Http404)
        or isinstance(exc, NotFound)
    ):
        return Response(
            response_wrapper(
                data={"error": "Not found."}, success=False, code=404
            ),
            status=status.HTTP_404_NOT_FOUND,
        )

    if response is not None:
        return response
