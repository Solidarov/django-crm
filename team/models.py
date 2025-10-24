from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    """
    Team within the CRM.

    Fields:
    - name: CharField(100)
    - members: ManyToMany to User (related_name='teams')
    - created_by: ForeignKey to User, CASCADE (related_name='created_teams')
    - created_at: DateTime auto-set on create

    - __str__ returns name
    """

    name = models.CharField(
        max_length=100,
    )
    members = models.ManyToManyField(
        User,
        related_name="teams",
    )
    created_by = models.ForeignKey(
        User,
        related_name="created_teams",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name
