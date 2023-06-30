from django.urls import path
from . import views

urlpatterns = [
    path('DappVinci/login/', views.login, name='login'),
    #path('register/', views.registration, name='registration')
    path('DappVinci/', views.homepage, name='home')
    ]