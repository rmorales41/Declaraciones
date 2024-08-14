from itertools import count
from django.http import JsonResponse
from django.shortcuts import render

from libreria.models import Asignacion, calendario_tributario


# redirecciona la consulta para abrir el formulario 
def VsPendiente_realizar(request):
   return render(request,'formas/Pendiente_Realizar.html')

# genera la informacion para mostrar los datos 
def VsPendiente_realizar_consultas(request,selectedYear, selectedMonth):
             
    try:                                                  
        ayear  = int(selectedYear)
        amonth = int(selectedMonth)
                                                
        Total_Declaraciones = calendario_tributario.objects.select_related(
            'IDDeclaracion',  # Unir con Declaracion
            'IDDeclaracion__asignacion',  # Unir con Asignacion a través de Declaracion
            'IDDeclaracion__asignacion__IDClientes_Proveedores',  # Unir con Clientes/Proveedores a través de Asignacion
            'IDDeclaracion__asignacion__IDPlanilla_Funcionarios'  # Unir con Planilla de Funcionarios a través de Asignacion
        ).prefetch_related(
            'IDDeclaracion__asignacion__historico_declaraciones'  # Prefetch para traer los historicos de declaraciones de Asignacion            
        ).filter(
            Fecha_Presenta__year=ayear,
            Fecha_Presenta__month=amonth,
            IDDeclaracion__estado = True 
        ).order_by("-IDDeclaracion")
        
       
         
 
        datadeclaracion = list(Total_Declaraciones.values(
            'IDDeclaracion',  # Acceder al ID de la declaración relacionada
            'IDDeclaracion__codigo',
            'IDDeclaracion__detalle',
            'IDDeclaracion__asignacion__IDAsignacion',
            'IDDeclaracion__asignacion__Fecha_Asigna',
            'IDDeclaracion__asignacion__Fecha_Presenta',
            'IDDeclaracion__asignacion__Fecha_Proxima',            
            'IDDeclaracion__asignacion__correo',
            'IDDeclaracion__asignacion__Iniciada',
            'IDDeclaracion__asignacion__Suspendida',
            'IDDeclaracion__asignacion__IDClientes_Proveedores__Descripcion',
            'IDDeclaracion__asignacion__IDPlanilla_Funcionarios__Nombre',
            'IDDeclaracion__estado',                    
        ))
                
                        
             
        return JsonResponse(datadeclaracion, safe=False)        
                                        
   
    
  


        return JsonResponse(datadeclaracion, safe=False)

    except calendario_tributario.DoesNotExist:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'El año proporcionado no es válido'}, status=400)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
