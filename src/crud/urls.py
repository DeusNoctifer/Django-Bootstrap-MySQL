from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('Iniciar-Sesion', views.sign_in, name='sign_in'),
    path('Registro/', views.sign_up, name='sign_up'),
    path('Cerrar-Sesion', views.sign_out, name='sign_out'),
    path('index', views.index, name='index'),
    
]