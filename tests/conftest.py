import pytest
import json
from django.test import Client
from django.urls import reverse
from rest_framework import status
from constants import PASSWORD, EMAIL, USERNAME, FIRST_NAME, LAST_NAME


@pytest.fixture
@pytest.mark.django_db
def create_user():
    c = Client()

    response = c.post(
        reverse("signup"),
        content_type="application/json",
        data=json.dumps(
            {
                "email": EMAIL,
                "username": USERNAME,
                "phone_number": "+34600000000",
                "password": PASSWORD,
                "password_confirmation": PASSWORD,
                "first_name": FIRST_NAME,
                "last_name": LAST_NAME,
            }
        ),
    )

    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["data"]
