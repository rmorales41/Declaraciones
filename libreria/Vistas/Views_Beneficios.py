# Vista de Beneficio 
from datetime import date, datetime, timedelta
from pyexpat.errors import messages
from urllib import request
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core import serializers
from django.core.mail import send_mail
from django.utils.timezone import now
from django.db.models import F 
from libreria import models
from libreria.forms import TipoForm
from libreria.models import Declaraciones_Tipo, Detalle_Declaracion_Tipo, cliente_proveedor_cliente_proveedor
import datetime


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
        detalle_id = request.POST.get('IDDetalleDeclaracionTipo', None)                       
        # Si detalle_id existe, intenta encontrar el detalle existente en la base de datos
        detalle_existente = None
        
        if detalle_id:
            detalle_existente = get_object_or_404(Detalle_Declaracion_Tipo, pk=detalle_id)        
        
        
        detalle = request.POST.get('detalle', '')  # Captura el valor del campo 'Detalle'
        fecha_solicitud = request.POST.get('fechasol', '') 
        numero_solicitud = request.POST.get('numero', '') 
        fecha_autorizacion = request.POST.get('fechaauto', '') 
        numero_autorizado = request.POST.get('numeroauto', '')         
        fecha_vencimiento = request.POST.get('fechavence', '') 
        fundamento_legal = request.POST.get('legal', '')  
        observaciones = request.POST.get('observaciones', '') 
        otorgado_por = request.POST.get('otorgado', '')  
        recordar_antes = request.POST.get('recuerda', '') 
        recordar_cada = request.POST.get('cada', '')  
        estado = request.POST.get('defaultCheck1', False) == 'True'
        # correo 
        usert = request.POST.get('usert', '')  # Obtener el usuario 
        domt = request.POST.get('domt', '')    # Obtener el dominio                         
        correo_notificar = usert + '@' + domt
        responsable = request.POST.get('responsable', '') 
        porcentaje = request.POST.get('porce', '')  
        informa = request.POST.get('informa', '')          
        imageno = request.FILES.get('inputGroupFile01', None)                                                                           
                

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
            detalle_existente.Imagen = imageno
            detalle_existente.IDClientes_Proveedores = cliente_proveedor        
            detalle_existente.IDDeclaraciones_Tipo = tipos_id   
             
            detalle_existente.save()
            messages.success(request, 'Actualizado correctamente')
        else:
            # Si no existe, crear una nueva instancia y guardarla
            print('aqui da el erro ')
            
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
                Imagen=imageno ,
                IDClientes_Proveedores=cliente_proveedor,    
                IDDeclaraciones_Tipo = tipos_id
            )
            nuevo_detalle_tipo.save()        
            messages.success(request, 'Creado Correctamente')                

        # Mostrar mensaje de éxito y redirigir        
        return redirect('Asigna_tipo')
        #return render(request, 'formas/Beneficios_Asigna_Tipos.html')
        
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

# muestra todos los registros activos para mostrar su imagen     
def VsBeneficios_Visor(request):      
    try:            
      # Obtener Beneficios y clientes  
        lista_beneficios= Detalle_Declaracion_Tipo.objects.filter(                      
          Estado = True ,                                                                                          
        ).values(  
                'IDClientes_Proveedores__IDClientes_Proveedores',   
                'IDClientes_Proveedores__Descripcion',
                'IDDetalle_Declaracion_Tipo',                  
                'Detalle',
                'Numero_autorizado',
                'Fecha_vencimiento',    
                'Imagen'
        ).order_by('Fecha_vencimiento')                        
        
        # Convertir el queryset en una lista de diccionarios
        datos = list(lista_beneficios) 
                                            
    except Exception as e:
        error_msg = f"Error en la vista VsVisor_Beneficios: {str(e)}"        
        return JsonResponse({'error': error_msg}, status=500) 
    
    return render(request,'formas/Visor_Beneficios.html',{'var_beneficios': datos  })    

# Busca las notificaciones     
def VsNotificaciones(request):
    hoy = now().date() # fecha de hoy 
    dias = 30
    try:          
        # muestra las lineas que cumplen 
        registros = Detalle_Declaracion_Tipo.objects.filter(
            Fecha_vencimiento__isnull=False,
            Estado=True                
        ).annotate(
            nombre_cliente = F('IDClientes_Proveedores__Descripcion')
        )   
        
        # crea el argumento para incluir los que cumplen 
        vencimientos = []
        
        for registro in registros:
            
            limite_vencimiento = registro.Fecha_vencimiento - timedelta(days=registro.Recordar_antes * dias)
            
            if hoy >= limite_vencimiento :    
                # Obtener el objeto de vencimiento desde la base de datos                
                registro.Fecha_Recordatorio = date.today()
                registro.Informa +=1 # suma uno mas 
                
                # actualiza estado de clientes                 
                registro.save()
                                        
                # registro para envio de correos 
                subject = f'Notificacion de Vencimientos, Modelo Declaraciones  :  {registro.nombre_cliente} - {registro.Detalle} '
                message = f"""                           Este es un recordatorio automático no lo responda.
                
                Por Favor Tome nota de cada correo es para indicarle que en nuestros registro hay movimientos 
                de Beneficios en clientes que estan pronto a vencer o ya estan vencidos verifique para que pueda 
                anticipar los datos con su cliente.
                
                El registro que le estamos indicando pertenece a  {registro.nombre_cliente} .
                 
                Resúmen ;
                
                1. Cliente en mención   : {registro.nombre_cliente} 
                2. Fecha de Vencimiento : {registro.Fecha_vencimiento}
                3. Autorizacion a buscar: {registro.Numero_autorizado}
                4. Veces Recordado      : {registro.Informa}
                5. Detalle registrado   : {registro.Detalle}
                6. Fecha Recordatorio   : {registro.Fecha_Recordatorio}
                
                Gracias y saludos, 
                Equipo de Notificaciones                
                
                """
                from_email = settings.EMAIL_HOST_USER # indica el usuario para lanzar correos 
                recipient_list = [registro.Correo_Notificar]
                
                # Enviar el correo electrónico
                send_mail(subject, message, from_email, recipient_list)
                
                vencimientos.append(registro)  
                
        return render(request,'formas/Beneficios_Notificaciones.html',{'v_notificaciones': vencimientos  })    
        
    except Exception as e:
        error_msg = f"Error en la vista VsNotificaciones: {str(e)}"
        return JsonResponse({'error': error_msg}, status=500)
    
    
# Busca las notificaciones controla el parametro de cada cuantas veces se debe de notificar para 
# efectos de un proceso automatico 
def VsNotificaciones2(request):
    hoy = now().date() # fecha de hoy 
    dias = 30
    try:          
        # muestra las lineas que cumplen 
        registros = Detalle_Declaracion_Tipo.objects.filter(
            Fecha_vencimiento__isnull=False,
            Estado=True                
        ).annotate(
            nombre_cliente = F('IDClientes_Proveedores__Descripcion')
        )   
        
        # crea el argumento para incluir los que cumplen 
        vencimientos = []
        
        for registro in registros:
            
            limite_vencimiento = registro.Fecha_vencimiento - timedelta(days=registro.Recordar_antes * dias)
            
            # validar el nulo 
            if registro.Recordar_cada is not None:
                dias_a_sumar = registro.Recordar_cada + 1
            else: 
                dias_a_sumar = 1   
            
            # si la fecha de recordatorio es nula            
            if registro.Fecha_Recordatorio is None:                
                registro.Fecha_Recordatorio = hoy - timedelta(days= registro.Recordar_antes)    
                                 
            print('recordatorio nul',registro.Fecha_Recordatorio)
            
            limite_fechaRecordatorio = registro.Fecha_Recordatorio + timedelta(days=dias_a_sumar)
            print('limite vencimiento',limite_vencimiento)
            print('recordatorio',limite_fechaRecordatorio)
            print('hoy',hoy)
            
            
            if hoy >= limite_vencimiento and   hoy >= limite_fechaRecordatorio :  
                    # Obtener el objeto de vencimiento desde la base de datos                
                    registro.Fecha_Recordatorio = date.today()
                    registro.Informa +=1 # suma uno mas 
                
                    # actualiza estado de clientes                 
                    registro.save()
                                        
                    # registro para envio de correos 
                    subject = f'Notificacion de Vencimientos, Modelo Declaraciones  :  {registro.nombre_cliente} - {registro.Detalle} '
                    message = f"""                           Este es un recordatorio automático no lo responda.

                    Por Favor Tome nota de cada correo es para indicarle que en nuestros registro hay movimientos 
                    de Beneficios en clientes que estan pronto a vencer o ya estan vencidos verifique para que pueda 
                    anticipar los datos con su cliente.
                
                    El registro que le estamos indicando pertenece a  {registro.nombre_cliente} .
                 
                    Resúmen ;
                
                    1. Cliente en mención   : {registro.nombre_cliente} 
                    2. Fecha de Vencimiento : {registro.Fecha_vencimiento}
                    3. Autorizacion a buscar: {registro.Numero_autorizado}
                    4. Veces Recordado      : {registro.Informa}
                    5. Detalle registrado   : {registro.Detalle}
                    6. Fecha Recordatorio   : {registro.Fecha_Recordatorio}
                
                    Gracias y saludos, 
                    Equipo de Notificaciones                
                
                """
                    from_email = settings.EMAIL_HOST_USER # indica el usuario para lanzar correos 
                    recipient_list = [registro.Correo_Notificar]
                
                    # Enviar el correo electrónico
                    send_mail(subject, message, from_email, recipient_list)
                
                    vencimientos.append(registro)  
                
        return render(request,'formas/Beneficios_Notificaciones.html',{'v_notificaciones': vencimientos  })    
        
    except Exception as e:
        error_msg = f"Error en la vista VsNotificaciones: {str(e)}"
        return JsonResponse({'error': error_msg}, status=500)    