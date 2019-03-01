import pytest
from rest_framework_jwt.settings import api_settings
from project.functions import is_valid_token
from project.users.models.users import User


@pytest.mark.django_db
def test_is_valid_token(create_user):
    user = User.objects.first()

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    assert is_valid_token(token) is True


@pytest.mark.django_db
def test_is_valid_token__invalid(create_user):
    invalid_token_1 = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmF"
        "tZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJ"
        "f36POk6yJV_adQssw5c"
    )

    invalid_token_2 = (
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI"
        "6Im1hcmNvc0BhZ3VheW8uZXMiLCJleHAiOjE1NTEzNzAxNzEsImVtYWlsIjoibWFyY29"
        "zQGFndWF5by5lcyIsIm9yaWdfaWF0IjoxNTUxMjgzNzcxfQ.sywLTCnxHdCSCMqcqlqG"
        "byWKgIpliGRMRuWXQWpCshk"
    )

    assert is_valid_token(invalid_token_1) is False
    assert is_valid_token(invalid_token_2) is False
