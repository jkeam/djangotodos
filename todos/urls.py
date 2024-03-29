from django.urls import path
app_name = 'todos'

from . import views
urlpatterns = [
    path('', views.TodoListView.as_view(), name='todo-view-list'),
    path('add/', views.TodoCreateView.as_view(), name='todo-add'),
    path('<int:pk>/', views.TodoUpdateView.as_view(), name='todo-update'),
    path('<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo-delete'),
    path('<int:pk>/toggle/', views.todo_toggle, name='todo-toggle'),
]
