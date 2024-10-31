from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.inicio, name ='inicio'),
    path ('procesadores/', views.lista_procesadores, name='lista_procesadores'),
    path ('procesadores/<int:numero_hilos>', views.lista_procesadores_segunhilos, name='lista_procesadores_segunhilos'),
    path ('procesadores/<nombre_familia>', views.lista_procesadores_segunfamilia, name='lista_procesadores_segunfamilia'),
    path('graficas/<nombre_familia>/<cantidad_vram>/', views.lista_graficas_segunfamilia_y_vram, name='lista_graficas_segunfamilia_y_vram'),] 


