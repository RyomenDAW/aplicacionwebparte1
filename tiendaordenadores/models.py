from django.conf import settings
from django.db import models
from django.utils import timezone

# Definir 10 modelos de mi página Web que cumpla los siguientes requisitos.
# Al menos 3 relaciones OneToOne, 3 relaciones ManytoOne, 3 relaciones ManyToMany


#====================================================================================

# Estos son mis 10 atributos de distinto tipo, se utilizaran en funcion.

# models.TextField
# models.CharField
# models.IntegerField
# models.FloatField
# models.BooleanField
# models.DateTimeField
# models.DateField
# models.URLField
# models.DecimalField
# models.EmailField

#El campo models.AutoField no lo contare, aun asi si lo menciono, ya que lo pondre
# en todo, como primary key
#====================================================================================


#Choices el segundo valor es el que se muestra
FAMILIA_PROCESADOR = (
    ("Ryzen", "Ryzen"),
    ("Intel", "Intel"),
)

FAMILIA_GRAFICA = (
    ("AMD", "AMD"),
    ("Nvidia", "NVIDIA"),
    ("Intel", "Intel")
)

SELLOCALIDAD_FUENTE = (
    ("80Bronce", "80Bronce"),
    ("80Silver", "80Silver"),
    ("80Gold", "80Gold"),
    ("80Plat", "80Plat"),
    ("80Titanium", "80Titanium"),
)

class Procesador (models.Model):
    id_procesador = models.AutoField(primary_key=True)
    nombre = models.TextField(max_length=100)
    familiaprocesador = models.TextField(max_length=6, choices=FAMILIA_PROCESADOR)
    potenciacalculo = models.CharField(max_length=30)
    nucleos = models.IntegerField(max_length=3)
    hilos = models.IntegerField(max_length=4)

class Grafica (models.Model):
    id_grafica = models.AutoField(primary_key=True)
    nombre = models.TextField(max_length=100)
    familiagrafica = models.TextField(max_length=6, choices=FAMILIA_PROCESADOR)
    potenciacalculo = models.CharField(max_length=30)
    memoriavram = models.CharField(max_length=10)
    fecha_salida = models.DateTimeField(default=timezone.now)

class FuenteAlimentacion(models.Model):
    id_fuente = models.AutoField(primary_key=True)
    vatios = models.TextField(max_length=4)
    amperaje = models.FloatField(max_length=20)
    fuentealimentacion = models.TextField(max_length=100)

class PlacaBase(models.Model):
    id_placabase = models.AutoField(primary_key=True)
    nombre = models.TextField(max_length=100)
    
    
placabase
monitor
ram
discodurohdd
discodurossd
discoduronvme
disipador


class Procesador (models.Model):
    models.URLField:



# (Al menos una de ella debe tener una tabla intermedia con atributos extras)
# Cada modelo debe tener al menos 4 campos.  Y debe existir en total 10 atributos 
# de distinto tipo.No son válidos los atributos de relaciones.

