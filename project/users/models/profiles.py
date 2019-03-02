from django.db import models
from project.models import BaseModel


class Profile(BaseModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    picture = models.ImageField(
        "profile picture", upload_to="users/pictures/", blank=True, null=True
    )
    biography = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return str(self.user)
