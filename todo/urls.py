from django.urls import path
from todo import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('todos', views.todos, name='todos'),
    path('todos/new', views.new_todo, name='new_todo'),
    path('todos/todo/<int:id>', views.todo_detail, name='todo_detail'),
    path('todos/update/<int:id>', views.update_todo, name='update_todo'),
    path('todos/delete/<int:id>', views.delete_todo, name='delete_todo'),
    path('todos/share/<int:id>/', views.share_todo, name='share_todo'),
    path('check-user/', views.check_user, name='check_user'),
    path('api/chart-data/', views.chart_data, name='chart_data'),
]
