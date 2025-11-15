from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# Custom User
class User(AbstractUser):
    # pass python keyword meand do nothin
    pass

class Status(models.TextChoices):
    TODO = 'TODO', 'To do'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    DONE = 'DONE', 'Done'

# Todo Model
class Todo(models.Model):    
    title = models.CharField(max_length=60)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    # created user
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    