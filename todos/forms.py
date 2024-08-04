from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .models import Todo, TodoComment
from django.utils.translation import gettext_lazy as _
Horizon = Todo.Horizon

class ImportTodosForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'file-input', 'x-on:change.debounce': 'afterFilepicked($event)'}
        )
    )

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
        return todo.name

class TodoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        children = kwargs.pop('children')
        children_label = kwargs.pop('children_label')
        initial_children = kwargs.pop('initial_children')
        parents = kwargs.pop('parents')
        parent_label = kwargs.pop('parent_label')
        initial_parents = kwargs.pop('initial_parents')
        super(TodoForm, self).__init__(*args, **kwargs)
        self.fields['children'].queryset = children
        self.fields['children'].label = f"Children {children_label}"
        self.fields['children'].initial = initial_children
        self.fields['parents'].queryset = parents
        self.fields['parents'].label = f"Parent {parent_label}"
        self.fields['parents'].initial = initial_parents

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
        required=True,
        widget=forms.HiddenInput()
    )

    children = CustomChildren(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    parents = CustomChildren(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Todo
        fields = ['name', 'description', 'due_date', 'horizon', 'children', 'parents']

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
