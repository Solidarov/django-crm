from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Database model for user profile. Contains fields:
        - 'user' one-to-one rel to model User
    """
    user = models.OneToOneField(User, 
                                related_name='userprofile', 
                                on_delete=models.CASCADE,)
    