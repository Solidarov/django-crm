from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    """
        Database model for <b>Clients</b>. Fields:
        - name CharField
        - email EmailField
        - description TextField, can be blank/null
        - created_by ForeignKey with User model
        - created_at DateTimeField with auto_now_add
        - modified_at DateTimeField with auto_now
    """

    name = models.CharField(max_length=255,)
    email = models.EmailField()
    description = models.TextField(blank=True,
                                   null=True,)
    created_by = models.ForeignKey(User, 
                                   related_name='clients',
                                   on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True,)
    modified_at = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return self.name