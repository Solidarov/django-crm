from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from team.models import Team


class ClientQuerySet(models.QuerySet):
    def get_for_user(self, user):
        """
        Return all client records related to the given user.

        Includes:
        - clients created by the user,
        - clients assigned to teams the user is a member of,
        - clients assigned to teams created by the user.
        """
        q_created_by = Q(created_by=user)  # client created by user
        q_teams_in = Q(team__in=user.teams.all())  # client in the same team as user
        q_teams_created = Q(
            team__in=user.created_teams.all()
        )  # client in the team created by user

        query = q_created_by | q_teams_in | q_teams_created

        return self.filter(query).distinct()


class ClientManager(models.Manager):
    def get_queryset(self):
        """
        Return a ClientQuerySet instance for this manager.
        """
        return ClientQuerySet(self.model, using=self._db)

    def get_for_user(self, user):
        """
        Delegate to ClientQuerySet.get_for_user(user).
        """
        return self.get_queryset().get_for_user(user=user)


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

    objects = ClientManager()

    def __str__(self):
        return self.name
