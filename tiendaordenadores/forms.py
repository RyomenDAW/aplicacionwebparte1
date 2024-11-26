from django import forms
from .models import Procesador

class ProcesadorForm(forms.ModelForm): #MODEL FORM
    class Meta:
        model = Procesador
        fields = 'nombre', 'urlcompra', 'familiaprocesador', 'potenciacalculo', 'nucleos', 'hilos', 'placabase'  # Incluir todos los campos del modelo

        # Configuración opcional para personalizar etiquetas o mensajes de ayuda
        labels = {
            'nombre': 'Nombre del Procesador',
            'urlcompra': 'URL de compra',
            'familiaprocesador': 'Familia del Procesador',
            'potenciacalculo': 'Potencia de Cálculo',
            'nucleos': 'Número de Núcleos',
            'hilos': 'Número de Hilos',
            'placabase': 'Placa Base',
        }
        help_texts = {
            'familiaprocesador': 'Selecciona la familia a la que pertenece el procesador, sea Intel o Ryzen',
            'urlcompra': 'Introduce una URL válida donde se pueda comprar este procesador.',
        }