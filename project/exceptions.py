from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):  # type: ignore
    """
    Custom exception handler for rest api views
    """

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        return response
