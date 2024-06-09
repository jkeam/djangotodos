from django import forms
from .models import Todo, TodoComment
from django.utils.translation import gettext_lazy as _
Horizon = Todo.Horizon

class TodoCommentForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder': 'Comment', 'class': 'textarea'}
    ))
    class Meta:
        model = TodoComment
        fields = ['body']

class CustomChildren(forms.ModelMultipleChoiceField):
    def label_from_instance(self, todo):
        return f"{todo.name} - {todo.description}"

class TodoChildrenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        hor = kwargs.pop('horizon')
        super(TodoChildrenForm, self).__init__(*args, **kwargs)
        match hor:
            case "PR":
                horizon_enum = Horizon.ACTIONS
            case "FO":
                horizon_enum = Horizon.PROJECTS
            case "GO":
                horizon_enum = Horizon.FOCUS
            case "VI":
                horizon_enum = Horizon.GOALS
            case "PR":
                horizon_enum = Horizon.VISIONS
            case "_":
                horizon_enum = Horizon.PURPOSE

        self.horizon = horizon_enum.value
        self.horizon_label = horizon_enum.label
        self.fields['children'].queryset = Todo.objects.filter(
            owner=self.request.user,
            horizon=self.horizon,
        )
        self.fields['children'].label = self.horizon_label

    children = CustomChildren(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Todo
        fields = ['children']

class TodoForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Name of task', 'class': 'input'}
    ))

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': 'Task Description', 'class': 'textarea'}
    ))

    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'class': 'input', 'type': 'date'}
    ))

    horizon = forms.ChoiceField(
        choices=Horizon.choices,
        required=False,
        widget=forms.Select()
    )

    class Meta:
        model = Todo
        fields = ['name', 'description', 'due_date', 'horizon']


class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Username', 'class': 'input'}
    ))

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'First Name', 'class': 'input'}
    ))

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Last Name', 'class': 'input'}
    ))

    class Meta:
        model = Todo
        fields = ['username', 'first_name', 'last_name']
