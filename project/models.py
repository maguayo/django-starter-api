import uuid
from django.db import models


class BaseModel(models.Model):
    """Base model Date

    BaseModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created = models.DateTimeField(
        "created at",
        auto_now_add=True,
        help_text="Date time on which the object was created.",
    )
    modified = models.DateTimeField(
        "modified at",
        auto_now=True,
        help_text="Date time on which the object was last modified.",
    )

    class Meta:
        abstract = True
        get_latest_by = "created"
        ordering = ["-created"]
