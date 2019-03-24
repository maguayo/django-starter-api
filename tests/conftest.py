import pytest
import json
from django.test import Client
from django.urls import reverse
from rest_framework import status
from constants import (
    PASSWORD,
    EMAIL,
    USERNAME,
    FIRST_NAME,
    LAST_NAME,
    PASSWORD_SECONDARY,
    EMAIL_SECONDARY,
    USERNAME_SECONDARY,
    FIRST_NAME_SECONDARY,
    LAST_NAME_SECONDARY,
)


@pytest.fixture
@pytest.mark.django_db
def create_user():
    c = Client()

    response = c.post(
        reverse("users-signup"),
        content_type="application/json",
        data=json.dumps(
            {
                "email": EMAIL,
                "username": USERNAME,
                "password": PASSWORD,
                "password_confirmation": PASSWORD,
            }
        ),
    )

    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["data"]


@pytest.fixture
@pytest.mark.django_db
def login_user(create_user):
    c = Client()

    response = c.post(
        reverse("users-login"),
        content_type="application/json",
        data=json.dumps({"email": EMAIL, "password": PASSWORD}),
    )
    body = response.json()["data"]

    return body["token"]


@pytest.fixture
@pytest.mark.django_db
def create_secondary_user():
    c = Client()

    response = c.post(
        reverse("users-signup"),
        content_type="application/json",
        data=json.dumps(
            {
                "email": EMAIL_SECONDARY,
                "username": USERNAME_SECONDARY,
                "password": PASSWORD_SECONDARY,
                "password_confirmation": PASSWORD_SECONDARY,
            }
        ),
    )

    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["data"]


@pytest.fixture
@pytest.mark.django_db
def login_secondary_user(create_secondary_user):
    c = Client()

    response = c.post(
        reverse("users-login"),
        content_type="application/json",
        data=json.dumps(
            {"email": EMAIL_SECONDARY, "password": PASSWORD_SECONDARY}
        ),
    )
    body = response.json()["data"]

    return body["token"]
