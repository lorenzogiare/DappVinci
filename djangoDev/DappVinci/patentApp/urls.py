from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('DappVinci/', views.homepage, name='home'),
    path('DappVinci/login/', views.userLogin, name='login'),
    path('DappVinci/logout/', views.userLogout, name='logout'),
    path('DappVinci/register/', views.registration, name='registration'),
    path('DappVinci/new-patent/', views.newPatent, name='create_new_patent'),
    path('DappVinci/read-patent/<int:pk>', views.readPatent, name='readPatent'),
    path('DappVinci/edit-patent/<int:pk>', views.editPatent, name='edit_patent'),
    ] 