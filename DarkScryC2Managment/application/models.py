from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # So we can reference the custom User
import uuid

class User(AbstractUser):
    """
    Custom Django user model with extra fields 
    (replacing your original SQLAlchemy-based 'User' table).
    """
    # By default, AbstractUser has 'username', 'password', 'email', 'is_staff', etc.
    # We'll add your custom fields:
    user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    role = models.CharField(max_length=20, default='user')
    otpuri = models.TextField(null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    # time_generated => optional: 
    # you can override 'date_joined' or define your own 
    time_generated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Agent(models.Model):
    AgentId = models.UUIDField(primary_key=True, editable=False, unique=True)
    HostName = models.CharField(max_length=255)
    Os = models.CharField(max_length=100)
    LastTimeUpdate = models.DateTimeField(auto_now_add=True)
    OnboardedTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.HostName