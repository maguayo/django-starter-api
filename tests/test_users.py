import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_create_user() -> None:
    c = Client()

    response = c.get(
        reverse("users-list"),
        content_type="application/json",
    )

    assert response.status_code == 200
