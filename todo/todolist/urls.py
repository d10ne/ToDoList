from django.urls import path
from .views import TaskList, TaskCreate, DeleteTask, LoginUser, logout_user, RegisterUser

urlpatterns = [
    path('', TaskList.as_view(), name='home'),
    path('add/', TaskCreate.as_view(), name='add'),
    path('delete/<int:pk>/', DeleteTask.as_view(), name='del'),
    path('accounts/login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]