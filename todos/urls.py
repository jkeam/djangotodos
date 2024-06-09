from django.urls import path
app_name = 'todos'

from . import views
urlpatterns = [
    path('', views.goto_horizon, name='root'),
    # horizons
    path('horizons/', views.HorizonListView.as_view(), name='horizon-view-list'),
    path('horizons/<str:pk>', views.HorizonDetailListView.as_view(), name='horizon-detail-list'),
    # profiles
    path('profiles/', views.ProfileUpdateView.as_view(), name='profile-detail'),
    # todos
    path('add/', views.TodoCreateView.as_view(), name='todo-add'),
    path('<int:pk>/', views.TodoView.as_view(), name='todo-view'),
    path('<int:pk>/update/', views.TodoUpdateView.as_view(), name='todo-update'),
    path('<int:pk>/toggle/', views.todo_toggle, name='todo-toggle'),
    path('<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo-delete'),
    path('<int:pk>/children/', views.TodoUpdateChildren.as_view(), name='todo-children'),
    # comments
    path('<int:pk>/comments/', views.TodoComments.as_view(), name='todo-comments'),
    path('<int:pk>/comments/add/', views.create_comment, name='todo-comments-add'),
    path('<int:todo_id>/comments/<int:pk>/delete/', views.TodoCommentDeleteView.as_view(), name='todo-comments-delete'),
    path('<int:todo_id>/comments/<int:pk>/update/', views.TodoCommentUpdateView.as_view(), name='todo-comments-update'),
]
