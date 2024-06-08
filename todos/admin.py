from django.contrib import admin
from .models import Todo, TodoComment

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'completed', 'due_date', 'created_at', 'updated_at', 'owner']
    list_filter = ['owner', 'completed', 'due_date', 'created_at', 'updated_at']
    search_fields = ['name', 'description']

@admin.register(TodoComment)
class TodoCommentAdmin(admin.ModelAdmin):
    list_display = ['body', 'created_at', 'updated_at', 'owner', 'todo']
    list_filter = ['owner', 'todo', 'created_at', 'updated_at']
    search_fields = ['body']
