from django.urls import path
app_name = 'todos'

from . import views
urlpatterns = [
    path('', views.goto_horizon, name='root'),
    # horizons
    path('horizons/', views.HorizonListView.as_view(), name='horizon-view-list'),
    path('horizons/<str:pk>', views.HorizonDetailListView.as_view(), name='horizon-detail-list'),
    path('horizons-partial/<str:pk>', views.HorizonDetailListPartialView.as_view(), name='horizon-detail-list-partial'),
    # profiles
    path('profiles/', views.ProfileUpdateView.as_view(), name='profile-detail'),
    path('change-password/', views.ChangePasswordView.as_view(), name='profile-password'),
    # tree todos
    path('tree/', views.tree_view, name='todo-tree'),
    path('tree-partial/<int:pk>', views.tree_view_partial, name='todo-tree-partial'),
    # todos
    path('add/', views.TodoCreateView.as_view(), name='todo-add'),
    path('<int:pk>/', views.TodoView.as_view(), name='todo-view'),
    path('<int:pk>/update/', views.TodoUpdateView.as_view(), name='todo-update'),
    path('<int:pk>/toggle-partial/', views.todo_toggle, name='todo-toggle-partial'),
    path('<int:pk>/blocked-partial/', views.todo_blocked, name='todo-blocked-partial'),
    path('<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo-delete'),
    path('<int:pk>/children/', views.TodoUpdateChildren.as_view(), name='todo-children'),
    path('<int:pk>/parents/', views.update_parents, name='todo-parents'),
    # comments
    path('<int:pk>/comments/', views.TodoComments.as_view(), name='todo-comments'),
    path('<int:pk>/comments/add/', views.create_comment, name='todo-comments-add'),
    path('<int:todo_id>/comments/<int:pk>/delete/', views.TodoCommentDeleteView.as_view(), name='todo-comments-delete'),
    path('<int:todo_id>/comments/<int:pk>/update/', views.TodoCommentUpdateView.as_view(), name='todo-comments-update'),
    # export
    path('export/', views.export_view, name='todo-export'),
]
