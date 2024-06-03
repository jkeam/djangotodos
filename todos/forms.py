from django import forms
from .models import Todo
Horizon = Todo.Horizon

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
