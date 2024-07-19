# Vista de Beneficio 
from  datetime import date, datetime 
from pyexpat.errors import messages
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core import serializers

from libreria.forms import TipoForm
from libreria.models import Declaraciones_Tipo, Detalle_Declaracion_Tipo, cliente_proveedor_cliente_proveedor

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

# asignacion de tipos  llena los dos select de clientes y tipos 
def Vsasigna_tipo(request):   
    try:
        # Obtener todos los clientes activos 
        lista_clientes = cliente_proveedor_cliente_proveedor.objects.filter(                      
          Estado = True ,          
          Tipo =  True                                                                        
        ).values(
            'IDClientes_Proveedores',
            'Descripcion',       
        ).order_by('Descripcion')
        
        
        # Convertir el queryset en una lista de diccionarios
        datos = list(lista_clientes)                
        # Retornar los datos como JsonResponse
        lista_tipos = Declaraciones_Tipo.objects.filter(
            Estado = True
        ).values(
            'IDDeclaraciones_Tipo',
            'Descripcion',
        )
        
        datos_tipo = list(lista_tipos)
        
      #  return JsonResponse(datos,datos_tipo safe=False)

    except Exception as e:
        error_msg = f"Error en la vista VsVisorTipos: {str(e)}"
        print(error_msg)  # Registrar el error en los registros de la aplicación
        return JsonResponse({'error': error_msg}, status=500) 
    
    return render(request,'formas/Beneficios_Asigna_Tipos.html',{'var_clientes': datos,'var_tipos': datos_tipo})

# guarda el tipo de beneficio por cliente 
def Vsguarda_tipo(request):
    if request.method == 'POST':
        
        # Obtener el ID del registro a actualizar si está presente en la solicitud        
        detalle_id = request.POST.get('datos.IDDetalle_Declaracion_Tipo', None)
        print(detalle_id)
        # Si detalle_id existe, intenta encontrar el detalle existente en la base de datos
        detalle_existente = None
        if detalle_id:
            detalle_existente = get_object_or_404(Detalle_Declaracion_Tipo, pk=detalle_id)        
        
        detalle = request.POST.get('detalle', '')  # Captura el valor del campo 'Detalle'
        numero_solicitud = request.POST.get('numero', '') 
        fecha_solicitud = request.POST.get('fechasol', '') 
        numero_autorizado = request.POST.get('numeroauto', '') 
        fecha_autorizacion = request.POST.get('fechaauto', '') 
        fecha_vencimiento = request.POST.get('fechavence', '') 
        estado = request.POST.get('defaultCheck1', False) == 'True'
        fundamento_legal = request.POST.get('legal', '')  
        observaciones = request.POST.get('observaciones', '') 
        otorgado_por = request.POST.get('otorgado', '')  
        recordar_antes = request.POST.get('recuerda', '') 
        recordar_cada = request.POST.get('cada', '')  
        responsable = request.POST.get('responsable', '') 
        porcentaje = request.POST.get('porce', '')  
        informa = request.POST.get('informa', '')  
        imageno = request.FILES.get('inputGroupFile01', None)  
        # correo 
        usert = request.POST.get('usert', '')  # Obtener el usuario 
        domt = request.POST.get('domt', '')    # Obtener el dominio 
        correo_notificar = usert + '@' + domt
        # datos del cliente 
        Clientes_id = request.POST.get('clientes_id')
        Tipos_id = request.POST.get('tipos_id')
       
        if recordar_antes == '':
             recordar_antes = 0
        else: 
            recordar_antes = int(recordar_antes) 
        
        if recordar_cada == '':
             recordar_cada = 0
        else: 
            recordar_cada = int(recordar_cada) 

        if informa == '':
             informa = 0
        else: 
            informa  = int(recordar_antes)                     

        # Validación y conversión de fechas
        try:
            fecha_solicitud = datetime.strptime(fecha_solicitud, '%Y-%m-%d').date() if fecha_solicitud else None
            fecha_autorizacion = datetime.strptime(fecha_autorizacion, '%Y-%m-%d').date() if fecha_autorizacion else None
            fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date() if fecha_vencimiento else None
            
        except ValueError:
            messages.error(request, 'Formato de fecha inválido. Utiliza YYYY-MM-DD.')
            return render(request, 'formas/Beneficios_Nuevo.html')

        cliente_proveedor = get_object_or_404(cliente_proveedor_cliente_proveedor, pk=Clientes_id)
        tipos_id = get_object_or_404(Declaraciones_Tipo, pk = Tipos_id )
        
         # Actualizar los campos del detalle existente si existe
        if detalle_existente:
            detalle_existente.Detalle = detalle
            detalle_existente.Fecha_solicitud = fecha_solicitud
            detalle_existente.Numero_solicitud = numero_solicitud
            detalle_existente.Fecha_autorizacion = fecha_autorizacion
            detalle_existente.Numero_autorizado = numero_autorizado
            detalle_existente.Fecha_vencimiento = fecha_vencimiento
            detalle_existente.Fundamento_Legal = fundamento_legal
            detalle_existente.observaciones = observaciones
            detalle_existente.Otorgadopor = otorgado_por
            detalle_existente.Recordar_antes = recordar_antes
            detalle_existente.Recordar_cada = recordar_cada
            detalle_existente.Estado = estado
            detalle_existente.Correo_Notificar = correo_notificar
            detalle_existente.Responsable = responsable
            detalle_existente.Porcentaje = porcentaje
            detalle_existente.Informa = informa
            detalle_existente.imagen = imageno
            detalle_existente.IDClientes_Proveedores = cliente_proveedor
            detalle_existente.IDDeclaraciones_Tipo = tipos_id
            detalle_existente.save()
            messages.success(request, 'Actualizado correctamente')
        else:
            # Si no existe, crear una nueva instancia y guardarla
            nuevo_detalle_tipo = Detalle_Declaracion_Tipo(
                Detalle=detalle,
                Fecha_solicitud=fecha_solicitud,
                Numero_solicitud=numero_solicitud,
                Fecha_autorizacion=fecha_autorizacion,
                Numero_autorizado=numero_autorizado,
                Fecha_vencimiento=fecha_vencimiento,
                Fundamento_Legal=fundamento_legal,
                observaciones=observaciones,
                Otorgadopor=otorgado_por,
                Recordar_antes=recordar_antes,
                Recordar_cada=recordar_cada,
                Estado=estado,
                Correo_Notificar=correo_notificar,
                Responsable=responsable,
                Porcentaje=porcentaje,
                Informa=informa,
                imagen=imageno,
                IDClientes_Proveedores=cliente_proveedor,
                IDDeclaraciones_Tipo=tipos_id,
            )
        
        
        
        # Crear una instancia del modelo Detalle_Declaracion_Tipo con los datos capturados
       # nuevo_detalle_tipo = Detalle_Declaracion_Tipo(
        #    Detalle=detalle,
        #    Fecha_solicitud=fecha_solicitud,
        #    Numero_solicitud=numero_solicitud,            
        #    Fecha_autorizacion=fecha_autorizacion,   
        #    Numero_autorizado=numero_autorizado,
        #    Fecha_vencimiento=fecha_vencimiento,   
        #    Fundamento_Legal=fundamento_legal,
        #    observaciones=observaciones,
        #    Otorgadopor=otorgado_por,
        #    Recordar_antes= recordar_antes,
        #    Recordar_cada= recordar_cada,
        #    Estado=estado,
        #    Correo_Notificar=correo_notificar,
        #    Responsable=responsable,
        #    Porcentaje=porcentaje,
        #    Informa=informa,
        #    imagen=imageno,
        #    IDClientes_Proveedores= cliente_proveedor,
        #    IDDeclaraciones_Tipo = tipos_id,
       # )                  
    
        # Guardar la instancia del modelo en la base de datos
        nuevo_detalle_tipo.save()

        # Mostrar mensaje de éxito y redirigir
        messages.success(request, 'Creado Correctamente')
        return redirect('visor')
  
        
    # Si el método no es POST o si hay errores en el formulario, renderiza el formulario vacío o con errores
    return render(request, 'formas/Beneficios_Nuevo.html')

# busca las referencias de los beneficios por cliente 
def Vsbusca_beneficios(request,IDD):              
    try:        
        
        lista_beneficios = Detalle_Declaracion_Tipo.objects.filter(
            IDClientes_Proveedores = IDD 
        ).values(         
            'IDDetalle_Declaracion_Tipo',
            'IDDeclaraciones_Tipo__Descripcion',         
            'Fecha_vencimiento', 
            'Numero_solicitud',
            'Numero_autorizado',
            'Detalle' ,            
            'Estado',            
            ).order_by('Fecha_vencimiento')
        
        datos = list(lista_beneficios)

        # Retornar los datos como JsonResponse
        return JsonResponse(datos, safe=False)

    except Exception as e:
        error_msg = f"Error en la vista Vsbusca_beneficios: {str(e)}"
        print(error_msg)  # Registrar el error en los registros de la aplicación
        return JsonResponse({'error': error_msg}, status=500)
    
#boton de eliminar registro en los tipos de beneficios     
def Vseliminabeneficio(request,id):    
    beneficio= Detalle_Declaracion_Tipo.objects.get(IDDetalle_Declaracion_Tipo=id)
    beneficio.delete()    
    return redirect('visor')

def Vsobtener_datos_registro(reqest,id):
    try:
        datos_json = Detalle_Declaracion_Tipo.objects.get(IDDetalle_Declaracion_Tipo=id)
        datos_serializados = serializers.serialize('json', [datos_json, ])
        return JsonResponse(datos_serializados, safe=False)
    except Detalle_Declaracion_Tipo.DoesNotExist:
        return JsonResponse({'error': 'El objeto solicitado no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)