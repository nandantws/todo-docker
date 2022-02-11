from typing import Collection
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TodoCollection(models.Model):
    name = models.CharField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name +' > '+ self.created_by.first_name


class Todo(models.Model):

    STATUS_CHOICES = (
        ('1', 'Pending'),
        ('2', 'In Progress'),
        ('3', 'Completed'),
    )
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=40)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='1')
    collection = models.ForeignKey('TodoCollection',related_name="todo",on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title
