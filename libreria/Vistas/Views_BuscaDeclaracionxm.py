import json
from datetime import datetime 
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from libreria.models import calendario_tributario, declaracion


# Vista BuscaDeclaracionxm 
def VsBuscadeclaracionxm(request, selectedYear,selectedMonth):    
   # an_Selecionado = int(anSeleccionada) # convierte el año        
    try:                    
        an = int(selectedYear) 
        me = int(selectedMonth)
                         
        
        Total_Declaraciones = calendario_tributario.objects.filter(Fecha_Presenta__year = an,Fecha_Presenta__month = me 
        ).order_by("-Fecha_Presenta")                      
            
        datadeclaracion = list(Total_Declaraciones.values(
            'IDCalendario_tributario',            
            'IDDeclaracion__codigo',
            'IDDeclaracion__detalle',
            'Fecha_Presenta',
            'IDDeclaracion__tiempo',
            'IDDeclaracion__IDDeclaracion',                      
        ))
     
        # Convertir a JSON usando serializers para incluir el campo IDDeclaracion__IDDeclaracion
      #  data = serializers.serialize('json', Total_Declaraciones, fields=('IDCalendario_tributario', 'IDDeclaracion__codigo', 'IDDeclaracion__detalle', 'Fecha_Presenta', 'IDDeclaracion__tiempo', 'IDDeclaracion__IDDeclaracion'))
     
             
        return JsonResponse(datadeclaracion, safe=False)        
                                        
    except calendario_tributario.DoesNotExist:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'El año proporcionado no es válido'}, status=400)
    except Exception as e:
        print(f"Error: {e}")  # Imprime el error en la consola
        return JsonResponse({'error': str(e)}, status=500)   

# realiza la inclusion de la nueva declaracion al calendario de declaraciones preparando el proximo año    
# reasignacion de declaraciones 
def VsReasignaDeclaracionCalendario(request,fecha_propuesta):        
    if request.method == 'POST':                
                                                                                                                                      
        try:       
           datadeclaracion = json.loads(request.body.decode('utf-8'))   
           iddeclaracion_id = datadeclaracion.get('iddeclaracion') # pone la declaracion seleccionada            
           # Verificar si existe una instancia válida de declaracion con el ID proporcionado            
           fecha_propuesta = datadeclaracion.get('fecha_Presenta')   
        
           # Obtener la instancia de la declaración
           declaracion_instance = declaracion.objects.get(pk=iddeclaracion_id)
                             
           # Verificar si ya existe una entrada en calendario_tributario con esta declaración
           if calendario_tributario.objects.filter(
                IDDeclaracion = declaracion_instance,
                Fecha_Presenta = fecha_propuesta
                ).exists():                                
                    return JsonResponse({'error': 'Esta declaración ya está incluida en el calendario'}, status=400)                      
           else:                       
                nueva_declaracion_calendario = calendario_tributario.objects.create(
                    Fecha_Presenta=fecha_propuesta,                
                    Observaciones='N/A',
                    IDDeclaracion=declaracion_instance
                )                                                                            
                return JsonResponse({'message': 'Declaración incluida'}, status=201)
        except Exception as e:  
            print('Error:', str(e))          
            return JsonResponse({'error': 'Error al crear la nueva declaracion. '}, status=500)
    else:
       
        return JsonResponse({'error': 'Método no permitido'}, status=405)    