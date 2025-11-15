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
    # created user(owner of the todo)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)
    # many-to-many relationship b/w User and Todo
    # One todo can be shared with many users
    # One user can have many shared todos
    # related_name='shared_todos' - Allows us to access shared todos from a user:
    # user.shared_todos.all() gets all todos shared with this user
    # blank=True - Makes this field optional (todos don't have to be shared)
    shared_with = models.ManyToManyField(User, related_name='shared_todos', blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    