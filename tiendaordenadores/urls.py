from django.urls import path, re_path
from . import views
from .views import *
from .views import oidc_callback

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
# urls.py
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/', views.inicio, name ='inicio'),
    path('', views.inicio, name='inicio'),  # Página de inicio
    #=====================================================================================================================================
    path ('procesadores/', views.lista_procesadores, name='lista_procesadores'),
    path ('procesadores/<int:numero_hilos>', views.lista_procesadores_segunhilos, name='lista_procesadores_segunhilos'),
    path ('procesadores/<nombre_familia>', views.lista_procesadores_segunfamilia, name='lista_procesadores_segunfamilia'),
    re_path(r'^graficas/(?P<nombre_familia>[-\w]+)/(?P<cantidad_vram>[-\w\.]+)/$', views.lista_graficas_segunfamilia_y_vram, name='lista_graficas_segunfamilia_y_vram'),
    path('procesadores/promedio-nucleos/', views.promedio_nucleos, name='promedio_nucleos'),
    path('graficas/filtrargraficas_segunvram', views.filtrargraficas_segunfecha, name ='filtrargraficas_segunvram'),
    path('ssd/primeros_5_ssd', views.primeros_5_ssd, name='primeros_5_ssd'),
    path('intermedia/graficas_sin_cuello_de_botella' ,views.graficas_sin_cuello_de_botella, name='graficas_sin_cuello_de_botella'),
    path('reverse/procesadores_segun_grafica/<int:grafica_id>', views.procesadores_segun_grafica, name='procesadores_segun_grafica'),
    path('graficas/lista_graficas.html', views.lista_graficas, name='lista_graficas'),
    #=====================================================================================================================================
    path('procesadores/crear_procesador/', views.crear_procesador, name='crear_procesador'),
    path('procesadores/read_procesadores/', views.read_procesadores, name='read_procesadores'),
    path('editar_procesador/<int:id_procesador>/', views.editar_procesador, name='editar_procesador'),
    path('procesadores/eliminar_procesador/<int:id_procesador>/', views.eliminar_procesador, name='eliminar_procesador'),   
    #=====================================================================================================================================
    path('procesadores/crear_grafica/', views.crear_grafica, name='crear_grafica'),
    path('procesadores/read_graficas/', views.read_graficas, name='read_graficas'),
    path('editar_grafica/<int:id_grafica>/', views.editar_grafica, name='editar_grafica'),
    path('graficas/eliminar_grafica/<int:id_grafica>/', views.eliminar_grafica, name='eliminar_grafica'),   
    #===================================================================================================================================== 
    path('monitores/crear_monitor/', views.crear_monitor, name='crear_monitor'),
    path('monitores/read_monitor/', views.read_monitor, name='read_monitor'),
    path('monitores/editar_monitor/<int:id_monitor>/', views.editar_monitor, name='editar_monitor'),
    path('monitores/eliminar_monitor/<int:id_monitor>/', views.eliminar_monitor, name='eliminar_monitor'),
    #=====================================================================================================================================    
    path('fuentes/crear_fuente/', views.crear_fuente, name='crear_fuente'),
    path('monitores/read_fuente/', views.read_fuente, name='read_fuente'),
    path('fuentes/editar_fuente/<int:id_fuente>/', views.editar_fuente, name='editar_fuente'),
    path('fuentes/eliminar_fuente/<int:id_fuente>/', views.eliminar_fuente, name='eliminar_fuente'),  
    #===================================================================================================================================== 
    path('ram/crear_ram/', views.crear_ram, name='crear_ram'),
    path('buscar_ram/', views.read_ram, name='read_ram'),
    path('ram/editar_ram/<int:id_ram>/', views.editar_ram, name='editar_ram'),
    path('ram/eliminar_ram/<int:id_ram>/', views.eliminar_ram, name='eliminar_ram'),  
    #=====================================================================================================================================  
    path('discoshdd/crear_hdd/', views.crear_hdd, name='crear_hdd'),
    path('discoshdd/read_hdd/', views.read_hdd, name='read_hdd'),
    path('discoshdd/editar_hdd/<int:id_hdd>/', views.editar_hdd, name='editar_hdd'),
    path('discoshdd/eliminar_hdd/<int:id_hdd>/', views.eliminar_hdd, name='eliminar_hdd'),    
    #=====================================================================================================================================
    path('registrar',views.registrar_usuario, name='registrar_usuario'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Ruta para el logout
    #=====================================================================================================================================
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #=====================================================================================================================================
    path("callback/", oidc_callback, name="oidc_callback"),
    
    ] 




# Sirve archivos de media en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)