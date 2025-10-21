from django.db import models
from django.contrib.auth.models import User

class Lead(models.Model):
    """
    Database model for <b>Leads</b>. Fields:
        - name CharField
        - email EmailField
        - description TextField, can be blank/null
        - priority CharField with choices (Low/Medium/High)
        - status CharField with choices (New/Contacted/Won/Lost)
        - created_by ForeignKey with User model
        - created_at DateTimeField with auto_now_add
        - modified_at DateTimeField with auto_now
    """

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    CHOICES_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High')
    )

    NEW = 'new'
    CONTACTED = 'contacted' 
    WON = 'won'
    LOST = 'lost'

    CHOICES_STATUS = (
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (WON, 'Won'),
        (LOST, 'Lost'),
    )

    name = models.CharField(max_length=255,)
    email = models.EmailField()
    description = models.TextField(blank=True,
                                   null=True)
    priority = models.CharField(max_length=10, 
                                choices=CHOICES_PRIORITY,
                                default=MEDIUM,)
    status = models.CharField(max_length=10,
                              choices=CHOICES_STATUS,
                              default=NEW,)
    created_by = models.ForeignKey(User, 
                                   related_name='leads',
                                   on_delete=models.CASCADE,)
    created_by = models.DateTimeField(auto_now_add=True,)
    modified_at = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return self.name