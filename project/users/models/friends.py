from django.db import models
from project.users.models.users import User
from project.models import BaseModel


class Friend(BaseModel):
    user = models.ForeignKey(
        User, related_name="friend_from", on_delete=models.CASCADE
    )
    friend = models.ForeignKey(
        User, related_name="friend_to", on_delete=models.CASCADE
    )
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(blank=True, null=True)
