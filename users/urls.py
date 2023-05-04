from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('changeInfo/', views.ChageInfo, name='changeinfo'),
]