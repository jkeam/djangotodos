from django.urls import path
app_name = 'todos'

from . import views
urlpatterns = [
    path('', views.goto_horizon, name='root'),
    path('horizons/', views.HorizonListView.as_view(), name='horizon-view-list'),
    path('horizons/<str:pk>', views.HorizonDetailListView.as_view(), name='horizon-detail-list'),
    path('add/', views.TodoCreateView.as_view(), name='todo-add'),
    path('profiles/', views.ProfileUpdateView.as_view(), name='profile-detail'),
    path('<int:pk>/', views.TodoUpdateView.as_view(), name='todo-update'),
    path('<int:pk>/children/', views.TodoUpdateChildren.as_view(), name='todo-update-children'),
    path('<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo-delete'),
    path('<int:pk>/toggle/', views.todo_toggle, name='todo-toggle'),
]
