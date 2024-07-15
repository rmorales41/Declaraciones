# Vista de Beneficio 
from pyexpat.errors import messages
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from libreria.forms import TipoForm
from libreria.models import Declaraciones_Tipo, cliente_proveedor_cliente_proveedor

def Vspyme(request):
     return render(request,'formas/Beneficios_Mantenimiento.html') 


def VsClientesActivos(request):
     return render(request,'formas/Visor_Clientes.html') 
 
 
def VsVisorClientes(request):    
    try:
        # Obtener todos los clientes activos 
        clientes_lista = cliente_proveedor_cliente_proveedor.objects.filter(
            Tipo=True,
            Estado = True 
        ).values(
            'IDClientes_Proveedores',
            'Descripcion',
            'Direccion',
            'Email',
            'Fecha_Ult_Movimiento',            
            ).order_by('Descripcion')

        # Convertir el queryset en una lista de diccionarios
        datos = list(clientes_lista)

        # Retornar los datos como JsonResponse
        return JsonResponse(datos, safe=False)

    except Exception as e:
        error_msg = f"Error en la vista VsDetalleClienteColaborador: {str(e)}"
        print(error_msg)  # Registrar el error en los registros de la aplicación
        return JsonResponse({'error': error_msg}, status=500)
 
 
def VsVisorTipos(request):
    try:
        # Obtener todos los clientes activos 
        lista_tipos = Declaraciones_Tipo.objects.filter(                      
        ).values(
            'IDDeclaraciones_Tipo',
            'Descripcion',
            'Institucion',
            'Observacion',
            'Estado',            
        ).order_by('Descripcion')

        # Convertir el queryset en una lista de diccionarios
        datos = list(lista_tipos)        
        # Retornar los datos como JsonResponse
        return JsonResponse(datos, safe=False)

    except Exception as e:
        error_msg = f"Error en la vista VsVisorTipos: {str(e)}"
        print(error_msg)  # Registrar el error en los registros de la aplicación
        return JsonResponse({'error': error_msg}, status=500)
 
# Vista para crear nuevos tipos de condiciones de beneficios  
#def VsTipoformulario(request):
#    dato_formulario = VTipoformularioForm(request.POST or None, request.FILES or None)    
    
#    if dato_formulario.is_valid():             
#        dato_formulario.save()                                  
#        messages.success(request,'Creado Correctamente')
#        return redirect('visor')       
    
          
#    return render(request,'formas/Beneficios_Mant_Nuevo.html',{'var_formulario': dato_formulario}) 


# se crear la estructura para usarla en el crud del formulario 
#class VTipoformularioForm(forms.ModelForm):
#    print('llego a la clase')
#    class Meta:
#        db_table ="declaraciones_tipo"
#        model = Declaraciones_Tipo
#        fields = '__all__'

# Elimina Tipo
def elimina(request,IDD):
    decla= Declaraciones_Tipo.objects.get(IDDeclaraciones_Tipo=IDD)
    decla.delete()    
    return redirect('visor')

def NuevoTipo(request):     
    dato_formulario = TipoForm(request.POST or None, request.FILES or None)
    
    if dato_formulario.is_valid(): 
        print('Entre aqui')        
        dato_formulario.save()                                          
        messages.success(request,'Creado Correctamente')
        return redirect('Declara_Tipo')  
                        
    return render(request,'formas/Beneficios_Nuevo.html',{'var_formulario': dato_formulario}) 

# vista Editar 
def editartipo(request,idTipo ):        
    tp = Declaraciones_Tipo.objects.get(IDDeclaraciones_Tipo = idTipo)
    dato_formulario = TipoForm(request.POST or None, request.FILES or None, instance = tp )
    
    if dato_formulario.is_valid() and request.POST:         
        dato_formulario.save()
        messages.success(request,'Modificado Correctamente')
        return redirect('Declara_Tipo')
    
    return render(request,'formas/Beneficios_Editar.html',{'var_formulario': dato_formulario})