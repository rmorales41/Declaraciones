from django import forms 
from .models import Asignacion, declaracion, planillas_planilla_funcionarios,Declaraciones_Tipo

# se declara la estructura del formulario 
class DeclaraForm(forms.ModelForm):
    class Meta:
        db_table ="declara"
        model = declaracion
        fields = '__all__'


class DeclaraFuncionarios(forms.ModelForm):
    class Meta:
        db_tabla = "declaraFun"
        model = planillas_planilla_funcionarios
        fields = '__all__'


# formulario de asignaciones 
class AsignaDeclaraciones(forms.ModelForm):
    class Meta:
        db_tabla ="asignadecla"
        model = Asignacion
        fields = '__all__'
    

# se declara la estructura del formulario  de tipos
class TipoForm(forms.ModelForm):
    class Meta:
        db_table ="tipo"
        model = Declaraciones_Tipo
        fields = '__all__'