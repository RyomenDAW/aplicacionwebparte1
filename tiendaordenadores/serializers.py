from rest_framework import serializers
from .models import *
from .forms import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username','first_name']
        
class ProcesadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procesador 
        fields = '__all__'
    

class ProcesadorMejoradoSerializer(serializers.ModelSerializer):
    placabase = serializers.PrimaryKeyRelatedField(read_only=True)
    user  = UsuarioSerializer()
    class Meta:
        model = Procesador
        fields = ['id_procesador', 'urlcompra', 'nombre', 'familiaprocesador', 'potenciacalculo','nucleos','hilos','imagen','user','placabase']


# class Procesador (models.Model):
#     id_procesador = models.AutoField(primary_key=True)
#     urlcompra = models.URLField(max_length=100)
#     nombre = models.TextField(max_length=100)
#     familiaprocesador = models.TextField(max_length=6, choices=FAMILIA_PROCESADOR)
#     potenciacalculo = models.PositiveBigIntegerField()
#     nucleos = models.PositiveSmallIntegerField()
#     hilos = models.PositiveIntegerField(validators=[MinValueValidator(35000)])  # Este validator luego se suprime por el form y view xd
#     imagen = models.ImageField(upload_to='procesadores/', blank=True, null=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Aquí usamos CustomUser en lugar de User

#     # Relación OneToOne con PlacaBase
#     placabase = models.OneToOneField('PlacaBase', on_delete=models.CASCADE, null=True, blank=True)



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
      token = super().get_token(user)
      # Add custom claims
      token['username'] = user.username 
      token['email'] = user.email
      return token

