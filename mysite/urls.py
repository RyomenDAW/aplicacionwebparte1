"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tiendaordenadores.urls')),  # Reemplaza 'tu_aplicacion' por el nombre de tu aplicación
    path('accounts/', include('django.contrib.auth.urls')),
    path('oauth2/',include('oauth2_provider.urls',namespace ='oauth2_provider')),
    # path('oidc/', include('oidc_provider.urls', namespace='oidc_provider')), #Añadimos OIDC aqui tambien, urls.py de mysite.
    path('template-api/', include('tiendaordenadores.api_urls')),  # Asegúrate que esto está correcto


]

handler404 = 'tiendaordenadores.views.mi_error_404'
handler400 = 'tiendaordenadores.views.mi_error_400'
handler403 = 'tiendaordenadores.views.mi_error_403'
handler500 = 'tiendaordenadores.views.mi_error_500'
