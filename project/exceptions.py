from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from project.functions import response_wrapper
from rest_framework.exceptions import ValidationError



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
                data=response.data,
                success=False,
                code=response.status_code
            ),
            status=response.status_code
        )

    # if it is handled, just return the response
    if response is not None:
        return response

    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            response_wrapper(data=None, success=False, code=404),
            status=status.HTTP_404_NOT_FOUND
        )