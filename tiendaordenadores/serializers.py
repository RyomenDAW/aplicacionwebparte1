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
        