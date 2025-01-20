from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario  # Importa tu modelo personalizado

# Registra el modelo Usuario con la clase UserAdmin
admin.site.register(Usuario, UserAdmin)
