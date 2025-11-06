from django.db import models
from django.contrib.auth.models import User


class Plan(models.Model):
    """
    Plan within the CRM.

    Fields:
    - name: CharField(100)
    - price: IntegerField()
    - desription: TextField(blank, null)
    - max_leads: IntegerField()
    - max_clients: IntegerField()

    - __str__ returns name
    """

    name = models.CharField(max_length=50)
    price = models.IntegerField()
    desription = models.TextField(blank=True, null=True)
    max_leads = models.IntegerField()
    max_clients = models.IntegerField()

    def __str__(self):
        return self.name


class Team(models.Model):
    """
    Team within the CRM.

    Fields:
    - plan: ForeignKey
    - name: CharField(100)
    - members: ManyToMany to User (related_name='teams')
    - created_by: ForeignKey to User, CASCADE (related_name='created_teams')
    - created_at: DateTime auto-set on create

    - __str__ returns name
    """

    plan = models.ForeignKey(Plan, related_name="teams", on_delete=models.CASCADE)

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
