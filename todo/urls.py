from django.urls import path
from todo import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/new', views.new_todo, name='new_todo'),
    path('dashboard/todo/<int:id>', views.todo_detail, name='todo_detail'),
    path('dashboard/todo/update/<int:id>', views.update_todo, name='update_todo'),
    path('dashboard/todo/delete/<int:id>', views.delete_todo, name='delete_todo'),
]
