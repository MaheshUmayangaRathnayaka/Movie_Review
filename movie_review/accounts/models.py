import uuid
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=15)
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='user_avatars', default='user.jpg')

    def __str__(self) -> str:
        return f"Profile of {self.person.username}"