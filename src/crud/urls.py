from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('Iniciar-Sesion', views.sign_in, name='sign_in'),
    path('Registro/', views.sign_up, name='sign_up'),
    path('index', views.index, name='index'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('eliminar/<str:idProducto>', views.eliminar , name='eliminar_producto'),
    path('agregar_productos', views.agregar_productos, name='agregar_productos'),
    path('actualizar_producto/<str:idProducto>', views.actualizar_producto, name='actualizar_producto'),

