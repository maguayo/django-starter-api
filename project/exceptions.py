from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
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

    if response is not None:
        return response
