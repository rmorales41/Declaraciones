from django.contrib import admin

# se importa el modelo de models declaracion 
from .models import  declaracion,Asignacion, planillas_planilla_funcionarios

# se debe de registrar en el administrador 
# declaracion
admin.site.register(declaracion)

# asigna cliente, funcionarios a declaraciones 
admin.site.register(Asignacion)

# asigna empleados
admin.site.register(planillas_planilla_funcionarios)


