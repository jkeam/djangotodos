from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from csv import writer

class Todo(models.Model):
    class Horizon(models.TextChoices):
        ACTIONS = "AC", _("Action")
        PROJECTS = "PR", _("Project")
        FOCUS = "FO", _("Focus")
        GOALS = "GO", _("Goal")
        VISIONS = "VI", _("Vision")
        PURPOSE = "PU", _("Purpose")

    horizon = models.CharField(
        max_length=2,
        choices=Horizon,
        default=Horizon.ACTIONS,
    )
    name = models.CharField(max_length=32, null=False, blank=False)
    description = models.TextField(default='', max_length=512, null=False, blank=True)
    completed = models.BooleanField(default=False, null=False)
    blocked = models.BooleanField(default=False, null=False)
    due_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    children = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="parents")

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

    def horizon_below(self) -> (Horizon|None):
        match self.horizon:
            case "PR":
                return Todo.Horizon.ACTIONS
            case "FO":
                return Todo.Horizon.PROJECTS
            case "GO":
                return Todo.Horizon.FOCUS
            case "VI":
                return Todo.Horizon.GOALS
            case "PU":
                return Todo.Horizon.VISIONS
            case _:
                return None

    def horizon_above(self) -> (Horizon|None):
        match self.horizon:
            case "AC":
                return Todo.Horizon.PROJECTS
            case "PR":
                return Todo.Horizon.FOCUS
            case "FO":
                return Todo.Horizon.GOALS
            case "GO":
                return Todo.Horizon.VISIONS
            case "VI":
                return Todo.Horizon.PURPOSE
            case _:
                return None

    def write_to_csv(self, csv_writer, write_header:bool = False):
        if write_header:
            csv_writer.writerow([
                "Horizon",
                "Name",
                "Description",
                "Due Date",
                "Completed",
                "Blocked",
                "Created At",
                "Updated At",
                "Children Ids"
            ])
        csv_writer.writerow([
            self.horizon,
            self.name,
            self.description,
            self.due_date,
            self.completed,
            self.blocked,
            self.created_at,
            self.updated_at,
            [child.pk for child in self.children.all()],
        ])
        return csv_writer

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
