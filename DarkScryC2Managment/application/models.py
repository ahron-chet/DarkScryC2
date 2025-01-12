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
    

class ChatMessage(models.Model):
    """
    Stores a single message in the chat. 
    If your 'clientName' is something like 'Machine1', store it here as well.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Which user sent the message? 
    # If your chat can also store bot messages, you can allow user to be null or create a 'role' field.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='messages'
    )

    # Alternatively, if you want to store name of the 'client' or 'machine':
    client_name = models.CharField(max_length=100, null=True, blank=True)
    
    # 'role' could be 'user' or 'bot' or something
    ROLE_CHOICES = (
        ('user', 'User'),
        ('bot', 'Bot'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    message = models.TextField()  # The actual chat text or command
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.role}: {self.message[:30]}"
