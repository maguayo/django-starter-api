import pytest
import json
import jwt
from django.conf import settings
from django.test import Client
from django.urls import reverse
from rest_framework import status
from project.users.models.users import User
from constants import PASSWORD, EMAIL, USERNAME, FIRST_NAME, LAST_NAME


@pytest.mark.django_db
def test_user_login(create_user):
    c = Client()

    response = c.post(
        reverse("login"),
        content_type="application/json",
        data=json.dumps({"email": EMAIL, "password": PASSWORD}),
    )

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()


@pytest.mark.django_db
def test_user_login__invalid_credentials(create_user):
    c = Client()

    response = c.post(
        reverse("login"),
        content_type="application/json",
        data=json.dumps({"email": EMAIL, "password": "wrongpassword123"}),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_login__check_token(create_user):
    c = Client()

    response = c.post(
        reverse("login"),
        content_type="application/json",
        data=json.dumps({"email": EMAIL, "password": PASSWORD}),
    )
    body = response.json()
    decoded_token = jwt.decode(
        body["token"],
        settings.JWT_AUTH["JWT_SECRET_KEY"],
        algorithms=["HS256"],
    )
    assert decoded_token["username"] == EMAIL
    assert decoded_token["email"] == EMAIL
    assert decoded_token["user_id"] == User.objects.get(email=EMAIL).id


@pytest.mark.django_db
def test_user_update(create_user):
    c = Client()

    response = c.patch(
        reverse("user-detail", kwargs={"user_id": create_user["id"]}),
        content_type="application/json",
        data=json.dumps({"email": "new_email@marcosaguayo.com"}),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] == True
    assert response.json()["data"]["email"] == "new_email@marcosaguayo.com"


@pytest.mark.django_db
def test_profile_user_update(create_user):
    c = Client()
    biography = "Hello World!"

    response = c.patch(
        reverse("user-profile-detail", kwargs={"user_id": create_user["id"]}),
        content_type="application/json",
        data=json.dumps({"biography": biography}),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] == True
    assert response.json()["data"]["profile"]["biography"] == biography


@pytest.mark.django_db
def test_user_token__check(create_user):
    assert False


@pytest.mark.django_db
def test_user_token__refresh(create_user):
    assert False
