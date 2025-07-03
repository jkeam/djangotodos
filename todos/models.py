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

    class Progress(models.TextChoices):
        BACKLOG = "BA", _("Backlog")
        PLANNED = "PL", _("Planned")
        IN_PROGRESS = "IP", _("InProgress")

    horizon = models.CharField(
        max_length=2,
        choices=Horizon,
        default=Horizon.ACTIONS,
    )
    progress = models.CharField(
        max_length=2,
        choices=Progress,
        default=Progress.BACKLOG,
    )
    name = models.CharField(max_length=128, null=False, blank=False)
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
    def progress_value_to_name(progress:str) -> str:
        match progress:
            case "BA":
                return "Backlog"
            case "PL":
                return "Planning"
            case "IP":
                return "In Progress"

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
        return f"Todo {self.name} with description {self.description} at {self.horizon} by {self.owner.username}"

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

    def progress_name(self) -> str:
        return Todo.progress_value_to_name(self.progress)

    def is_backlog(self) -> bool:
        return self.progress == Todo.Progress.BACKLOG

    def is_planned(self) -> bool:
        return self.progress == Todo.Progress.PLANNED

    def is_in_progress(self) -> bool:
        return self.progress == Todo.Progress.IN_PROGRESS

    def write_to_csv(self, csv_writer, write_header:bool = False):
        if write_header:
            csv_writer.writerow([
                "Id",
                "Horizon",
                "Name",
                "Description",
                "Due Date",
                "Completed",
                "Blocked",
                "Progress",
                "Created At",
                "Updated At",
                "Children Ids"
            ])
        csv_writer.writerow([
            self.id,
            self.horizon,
            self.name,
            self.description,
            self.due_date,
            self.completed,
            self.blocked,
            self.progress,
            self.created_at,
            self.updated_at,
            [child.pk for child in self.children.all()],
        ])
        return csv_writer

    def read_from_csv(self, input):
        self.horizon = input['Horizon']
        self.name = input['Name']
        self.description = input['Description']
        input_due_date = input['Due Date']
        if input_due_date:
            self.due_date = input_due_date.strip()
        self.completed = input['Completed']
        self.blocked = input['Blocked']
        input_progress = input['Progress']
        if input_progress:
            self.progress = input_progress
        else:
            self.progress = Todo.Progress.BACKLOG
        self.created_at = input['Created At']
        self.updated_at = input['Updated At']
        return self

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
