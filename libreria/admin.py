from django.contrib import admin

# se importa el modelo de models declaracion 
from .models import declaracion

# se debe de registrar en el administrador 
# modelo declaracion para que pueda usar la base de datos 

# declaracion
admin.site.register(declaracion)

