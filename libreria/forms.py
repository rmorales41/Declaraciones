from django import forms 
from .models import declaracion

# se declara la estructura del formulario 
class DeclaraForm(forms.ModelForm):
    class Meta:
        model = declaracion
        fields = '__all__'
        
