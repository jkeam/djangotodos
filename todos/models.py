from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Todo(models.Model):
    class Horizon(models.TextChoices):
        ACTIONS = "AC", _("Actions")
        PROJECTS = "PR", _("Projects")
        FOCUS = "FO", _("Focus")
        GOALS = "GO", _("Goals")
        VISIONS = "VI", _("Visions")
        PURPOSE = "PU", _("Purpose")

    horizon = models.CharField(
        max_length=2,
        choices=Horizon,
        default=Horizon.ACTIONS,
    )
    name = models.CharField(max_length=32, null=False, blank=False)
    description = models.TextField(default='', max_length=512, null=False, blank=True)
    completed = models.BooleanField(default=False, null=False)
    due_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    children = models.ManyToManyField("self")

    @staticmethod
    def valid_horizon(hor:str) -> bool:
        return hor in ["AC", "PR", "FO", "GO", "VI", "PU"]

    @staticmethod
    def horizon_value_to_name(hor:str) -> str:
        match hor:
            case "PR":
                return "Projects"
            case "FO":
                return "Areas of Focus and Accountability"
            case "GO":
                return "One to Two Year Goals"
            case "VI":
                return "Three to Five Year Visions"
            case "PU":
                return "Principals and Purpose"
            case _:
                return "Actions"

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"Todo {self.name} by {self.owner.username}"


class TodoComment(models.Model):
    body = models.TextField(default='', max_length=512, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"Comment by {self.owner.username} on {self.post.name}"
