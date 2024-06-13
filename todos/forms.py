from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
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
        if todo.description:
            return f"{todo.name} - {todo.description}"
        else:
            return todo.name

class TodoChildrenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        children = kwargs.pop('children')
        label = kwargs.pop('label')
        super(TodoChildrenForm, self).__init__(*args, **kwargs)
        self.fields['children'].queryset = children
        self.fields['children'].label = label

    children = CustomChildren(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Todo
        fields = ['children']

class TodoParentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        parents = kwargs.pop('parents')
        label = kwargs.pop('label')
        super(TodoParentForm, self).__init__(*args, **kwargs)
        self.fields['parents'].queryset = parents
        self.fields['parents'].label = label

    parents = CustomChildren(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Todo
        fields = ['parent']

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

class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(
            attrs={'placeholder': '', 'class': 'input'}
    ))

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={'placeholder': '', 'class': 'input'}
    ))

    new_password2 = forms.CharField(
        label="New Password Confirmation",
        widget=forms.PasswordInput(
            attrs={'placeholder': '', 'class': 'input'}
    ))

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
        model = User
        fields = ['username', 'first_name', 'last_name']
