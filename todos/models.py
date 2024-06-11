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
    children = models.ManyToManyField("self", symmetrical=False)

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

    @staticmethod
    def horizon_value_to_horizon(hor:str) -> Horizon:
        match hor:
            case "PR":
                return Todo.Horizon.PROJECTS
            case "FO":
                return Todo.Horizon.FOCUS
            case "GO":
                return Todo.Horizon.GOALS
            case "VI":
                return Todo.Horizon.VISIONS
            case "PU":
                return Todo.Horizon.PURPOSE
            case _:
                return Todo.Horizon.ACTIONS

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"Todo {self.name} by {self.owner.username}"

    def horizon_name(self) -> str:
        return Todo.horizon_value_to_name(self.horizon)

    def is_contained_by(self) -> list:
        return Todo.objects.filter(children__in=[self.pk])

    def is_action_horizon(self) -> bool:
        return self.horizon == Todo.Horizon.ACTIONS

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
