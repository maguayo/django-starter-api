import jwt
from jwt.exceptions import InvalidSignatureError
from django.conf import settings


def response_wrapper(success, data, code=None):
    return {"success": success, "code": code, "data": data}


def is_valid_token(token):
    try:
        jwt.decode(
            token, settings.JWT_AUTH["JWT_SECRET_KEY"], algorithms=["HS256"]
        )
    except InvalidSignatureError:
        return False
    else:
        return True
