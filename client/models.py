from django.db import models
from django.contrib.auth.models import User

from team.models import Team


class Client(models.Model):
    """
    Database model for <b>Clients</b>. Fields:
    - team ForeignKey with Team model
    - name CharField
    - email EmailField
    - description TextField, can be blank/null
    - created_by ForeignKey with User model
    - created_at DateTimeField with auto_now_add
    - modified_at DateTimeField with auto_now
    """

    team = models.ForeignKey(
        Team,
        related_name="clients",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=255,
    )
    email = models.EmailField()
    description = models.TextField(
        blank=True,
        null=True,
    )
    created_by = models.ForeignKey(
        User,
        related_name="clients",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name
