from rest_framework import serializers
from .models import *
from .forms import *


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

class GraficaMejoradaSerializer(serializers.ModelSerializer):
    user = UsuarioSerializer()
    procesador = ProcesadorMejoradoSerializer(source='grafica_procesadores', read_only=True)
    placabase = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Grafica
        fields = ['id_grafica', 'urlcompra', 'nombre', 'familiagrafica', 'potenciacalculo', 
                  'memoriavram', 'fecha_salida', 'trazadorayos', 'user', 'procesador', 'placabase']
        
class FuenteAlimentacionMejoradaSerializer(serializers.ModelSerializer):
    user = UsuarioSerializer()
    class Meta:
        model = FuenteAlimentacion
        fields = ['id_fuente', 'urlcompra', 'vatios', 'amperaje', 
                  'conectoresdisponibles', 'calidadfuente', 'user']
        
        
class RamMejoradaSerializer(serializers.ModelSerializer):
    user = UsuarioSerializer()  

    class Meta:
        model = Ram
        fields = ['id_ram', 'fecha_fabricacion', 'mhz', 'familiaram', 'rgb', 
                  'factormemoria', 'user']       
        




#ESTA DE AQUI NO




# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#       token = super().get_token(user)
#       # Add custom claims
#       token['username'] = user.username 
#       token['email'] = user.email
#       return token
#       pass

