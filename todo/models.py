from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# Custom User
class User(AbstractUser):
    # pass python keyword meand do nothin
    pass


# Todo Model
class Todo(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # to associate the todo with a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    