from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("dashboard/", views.dashboard, name="dashboard"),  
    
]