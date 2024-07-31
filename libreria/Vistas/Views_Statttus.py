# ve el Status de las declaraciones junto con las fechas de los calendarios mes y año  
from urllib import request
from django.http import JsonResponse
from django.shortcuts import render

from libreria.models import Historico_Declaraciones


def Vslevanta_Stattus(request):
    return render(request,'formas/Stattus_Calendario.html') 
 
def VsDeclaracionesfinales(request,selectedYear,selectedMonth):               
    try:                    
        an = int(selectedYear) 
        me = int(selectedMonth)
                                 
        Total_Declaraciones = Historico_Declaraciones.objects.filter(
            Fecha_Presenta__year = an,
            Fecha_Presenta__month = me 
        ).order_by("-Fecha_Presenta")                      
            
        hdatadeclaracion = list(Total_Declaraciones.values(
            'IDHistorico_Declaraciones',            
            'IDasignacion',
            'Fecha_Presenta',            
        ))
     
        # Convertir a JSON usando serializers para incluir el campo IDDeclaracion__IDDeclaracion
        #  data = serializers.serialize('json', Total_Declaraciones, fields=('IDCalendario_tributario', 'IDDeclaracion__codigo', 'IDDeclaracion__detalle', 'Fecha_Presenta', 'IDDeclaracion__tiempo', 'IDDeclaracion__IDDeclaracion'))
     
        print(hdatadeclaracion)     
        return JsonResponse(hdatadeclaracion, safe=False)        
                                        
    except Historico_Declaraciones.DoesNotExist:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'El año proporcionado no es válido'}, status=400)
    except Exception as e:
        print(f"Error: {e}")  # Imprime el error en la consola
        return JsonResponse({'error': str(e)}, status=500)   