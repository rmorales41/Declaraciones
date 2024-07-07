from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from libreria.models import Asignacion, planillas_planilla_funcionarios


def VsCargaformula(request):
    return render(request,'formas/Visor_Funcionarios.html')  


def VsVisor_Funcionarios(request):
    try:  
        conteo = Asignacion.objects.values(            
            'IDPlanilla_Funcionarios',
            'IDPlanilla_Funcionarios__Nombre'
        ).annotate(
            total_asignaciones = Count('IDPlanilla_Funcionarios')
        ).order_by('IDPlanilla_Funcionarios')                         
        
        datos_conteo = list(conteo)
               
        # Retornar los datos como JsonResponse
        return JsonResponse(datos_conteo, safe=False)

    except Exception as e:
        print(f"Error en la vista VsVisor_Funcionarios: {e}")
        return JsonResponse({'error': str(e)}, status=500)