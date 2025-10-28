from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from team.models import Team


class LeadQuerySet(models.QuerySet):
    def get_for_user(self, user):
        """
        Return all lead records related to the given user.

        Includes:
        - leads created by the user (this covers leads with team=None created by the user),
        - leads assigned to teams the user is a member of,
        - leads assigned to teams created by the user.
        """
        q_created_by = Q(created_by=user)  # lead created by user
        q_teams_in = Q(team__in=user.teams.all())  # lead in the same team as user
        q_tems_created = Q(
            team__in=user.created_teams.all()
        )  # lead in the team created by user

        query = q_created_by | q_teams_in | q_tems_created

        return self.filter(query).distinct()


class LeadManager(models.Manager):
    def get_queryset(self):
        """
        Return a LeadQuerySet instance for this manager.
        """
        return LeadQuerySet(self.model, using=self._db)

    def get_for_user(self, user):
        """
        Delegate to LeadQuerySet.get_for_user(user).
        """
        return self.get_queryset().get_for_user(user=user)


class Lead(models.Model):
    """
    Database model for <b>Leads</b>. Fields:
        - team ForeignKey with Team model
        - name CharField
        - email EmailField
        - description TextField, can be blank/null
        - priority CharField with choices (Low/Medium/High)
        - status CharField with choices (New/Contacted/Won/Lost)
        - converted_to_client BooleanField
        - created_by ForeignKey with User model
        - created_at DateTimeField with auto_now_add
        - modified_at DateTimeField with auto_now
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    CHOICES_PRIORITY = (
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    )

    NEW = "new"
    CONTACTED = "contacted"
    WON = "won"
    LOST = "lost"

    CHOICES_STATUS = (
        (NEW, "New"),
        (CONTACTED, "Contacted"),
        (WON, "Won"),
        (LOST, "Lost"),
    )

    objects = LeadManager()

    team = models.ForeignKey(
        Team,
        related_name="leads",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=255,
    )
    email = models.EmailField()
    description = models.TextField(
        blank=True,
        null=True,
    )
    priority = models.CharField(
        max_length=10,
        choices=CHOICES_PRIORITY,
        default=MEDIUM,
    )
    status = models.CharField(
        max_length=10,
        choices=CHOICES_STATUS,
        default=NEW,
    )
    converted_to_client = models.BooleanField(
        default=False,
    )
    created_by = models.ForeignKey(
        User,
        related_name="leads",
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
