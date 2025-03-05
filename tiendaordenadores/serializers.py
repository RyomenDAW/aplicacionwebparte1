from rest_framework import serializers
from .models import *
from .forms import *


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username','first_name']
        
class ProcesadorSerializer(serializers.ModelSerializer):
    user = UsuarioSerializer(read_only=True)  # 🔥 Se muestra en GET pero no se espera en POST

    class Meta:
        model = Procesador 
        fields = '__all__'  # 🔥 Incluir user, pero no hacerlo obligatorio en POST

    def create(self, validated_data):
        """ Sobreescribir create para asignar user automáticamente """
        request = self.context.get("request")  # 🔥 Obtener la request desde el contexto
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user  # 🔥 Asignar el usuario autenticado
        return super().create(validated_data)
    
    
from rest_framework import serializers
from .models import Usuario
from django.contrib.auth.hashers import make_password

class UsuarioSerializerRegistro(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ("username", "email", "password1", "password2", "first_name", "last_name", "rol")

    def validate_username(self, username):
        if Usuario.objects.filter(username=username).exists():
            raise serializers.ValidationError("Ya existe un usuario con este nombre.")
        return username

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": "Las contraseñas no coinciden."})
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        validated_data["password1"] = make_password(validated_data["password1"])
        user = Usuario.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password1"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            rol=validated_data.get("rol", 2),  # Cliente por defecto
        )
        return user

    
class PlacaBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacaBase
        fields = '__all__'

class ProcesadorMejoradoSerializer(serializers.ModelSerializer):
    placabase = serializers.PrimaryKeyRelatedField(read_only=True)
    user  = UsuarioSerializer()
    class Meta:
        model = Procesador
        fields = ['id_procesador', 'urlcompra', 'nombre', 'familiaprocesador', 'potenciacalculo','nucleos','hilos','imagen','user','placabase']
#===============================================================================================================================================================
class GraficaMejoradaSerializer(serializers.ModelSerializer):
    user = UsuarioSerializer()
    procesador = ProcesadorMejoradoSerializer(source='grafica_procesadores', read_only=True)
    placabase = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Grafica
        fields = ['id_grafica', 'urlcompra', 'nombre', 'familiagrafica', 'potenciacalculo', 
                  'memoriavram', 'fecha_salida', 'trazadorayos', 'user', 'procesador', 'placabase']

    def validate_potenciacalculo(self, value):
        if value < 0:
            raise serializers.ValidationError("La potencia de cálculo no puede ser negativa.")
        return value
#===============================================================================================================================================================
class FuenteAlimentacionMejoradaSerializer(serializers.ModelSerializer):
    user = UsuarioSerializer()

    class Meta:
        model = FuenteAlimentacion
        fields = ['id_fuente', 'urlcompra', 'vatios', 'amperaje', 
                  'conectoresdisponibles', 'calidadfuente', 'user']

    def validate_vatios(self, value):
        if value <= 0:
            raise serializers.ValidationError("Los vatios deben ser un valor mayor que cero.")
        return value
#===============================================================================================================================================================
class RamMejoradaSerializer(serializers.ModelSerializer):
    user = UsuarioSerializer()  

    class Meta:
        model = Ram
        fields = ['id_ram', 'fecha_fabricacion', 'mhz', 'familiaram', 'rgb', 
                  'factormemoria', 'user']

    def validate_mhz(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("La frecuencia de la RAM (MHz) no puede estar vacía.")
        return value
#===============================================================================================================================================================
#TAREA APIREST III


class CrearProcesadorSerializer(serializers.ModelSerializer):
    """ SERIALIZER PARA LA CREACIÓN DE PROCESADORES """

    class Meta:
        model = Procesador 
        fields = ['urlcompra', 'nombre', 'familiaprocesador', 'potenciacalculo', 'nucleos', 'hilos', 'imagen']
    
    def validate_nombre(self, value):
        """ VALIDAR QUE EL NOMBRE NO CONTENGA SOLO NÚMEROS """
        if value.isdigit():
            raise serializers.ValidationError("EL NOMBRE NO PUEDE CONTENER SOLO NÚMEROS, I3, RYZEN 5, ETC")
        return value

    def validate_potenciacalculo(self, value):
        """ SI EL PROCESADOR TIENE MÁS DE 8 NÚCLEOS, SU POTENCIA DE CÁLCULO DEBE SER AL MENOS 1000 """
        nucleos = int(self.initial_data.get('nucleos', 0))  # OBTENER EL VALOR DE NÚCLEOS SIN SERIALIZACIÓN
        if nucleos > 8 and value < 1000:
            raise serializers.ValidationError("SI EL PROCESADOR TIENE MÁS DE 8 NÚCLEOS, LA POTENCIA DEBE SER AL MENOS 1000.")
        return value

    def validate_hilos(self, value):
        """ VALIDAR QUE EL NÚMERO DE HILOS SEA AL MENOS EL DOBLE DEL NÚMERO DE NÚCLEOS """
        nucleos = int(self.initial_data.get('nucleos', 0))
        if value < (nucleos * 2):
            raise serializers.ValidationError("EL NÚMERO DE HILOS DEBE SER AL MENOS EL DOBLE DEL NÚMERO DE NÚCLEOS.")
        return value

    def create(self, validated_data):
        """ ASIGNAR AUTOMÁTICAMENTE EL USUARIO AUTENTICADO AL CREAR UN PROCESADOR """
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user  # ASIGNAR EL USUARIO AUTENTICADO
        return super().create(validated_data)




class ProcesadorActualizarNombreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procesador
        fields = ['nombre']  # Solo permitimos actualizar este campo

    def validate_nombre(self, nombre):
        """Validar que el nombre no esté repetido"""
        procesador_existente = Procesador.objects.filter(nombre=nombre).first()
        if procesador_existente and procesador_existente.id != self.instance.id:
            raise serializers.ValidationError("Ya existe un procesador con ese nombre.")
        return nombre

    
    
#===============================================================================================================================================================



class CrearGraficaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grafica
        fields = ['urlcompra', 'nombre', 'familiagrafica', 'potenciacalculo', 'memoriavram', 'trazadorayos', 'grafica_procesadores']

    def validate_nombre(self, value):
        """ Validar que el nombre de la gráfica sea único """
        if Grafica.objects.filter(nombre=value).exists():
            raise serializers.ValidationError("Ya existe una gráfica con este nombre.")
        return value

    def validate_potenciacalculo(self, value):
        """ Validar que la potencia de cálculo sea mayor a 0 """
        if value <= 0:
            raise serializers.ValidationError("La potencia de cálculo debe ser mayor a 0.")
        return value

    def validate_memoriavram(self, value):
        """ Validar que la memoria VRAM no sea negativa """
        if value < 0:
            raise serializers.ValidationError("La memoria VRAM no puede ser negativa.")
        return value


class MonitorGraficaSerializer(serializers.ModelSerializer):
    """ Serializador para la relación Monitor-Grafica """

    class Meta:
        model = MonitorGrafica
        fields = "__all__"  # Incluye todos los campos de la relación Monitor-Grafica
        
        
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#       token = super().get_token(user)
#       # Add custom claims
#       token['username'] = user.username 
#       token['email'] = user.email
#       return token
#       pass

