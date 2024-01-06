from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False)
    description = models.TextField(default='', max_length=512,null=False, blank=True)
    completed = models.BooleanField(default=False, null=False)
    due_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    class Meta:
        ordering = ["-id"]
