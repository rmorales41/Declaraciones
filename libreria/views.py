from django.contrib.auth import authenticate, login , logout
from django.shortcuts import redirect
from ctypes import util
from datetime import date, timedelta
from datetime import datetime
import json
import subprocess
from typing import Self
from urllib import request
from django.contrib import messages
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
import psutil
from .models import Asignacion, Bitacora, Declaracion_Clientes, Historico_Declaraciones, LoginForm, calendario_tributario, declaracion, planillas_planilla_funcionarios,cliente_proveedor_cliente_proveedor,Historico_Declaraciones
from django.core.serializers import serialize
from django.core import serializers
from django.db.models import F,Q   
from django.utils.dateparse import parse_date
#from .forms import LoginForm

# la clase F funciona para filtrar productos mayores ejemplo productos = Producto.objects.filter(precio__gt=F('descuento'))
# la clase Q funciona para generar consultas correctas 

# ingreso login al sistema 
def login_view(request):
    if request.method=='POST':
        form =LoginForm(request, data=request.POST)
       

        if form.is_valid():                   
            user = form.get_user()
            login(request,user)    
            
            #registro de ingreso a bitacora 
            usuario = user.first_name
            proceso = "Ingreso al Sistema"        
            descripcion = "El usuario logro el ingreso de su usuario al sistema."
            observaciones = "Ingreso Correcto se valido sin problema."
            modulo = "login"
            VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)
            
            return redirect('visor/')  # redirige   
        else:
            print('Error del formulario',form.errors)                              
    else:        
        form = LoginForm()            
   
    return render(request,'formas/login.html',{'form': form})

# salida del sistema 
def logout_view(request):
    logout(request)
    
    #registro de salida a bitacora 
    usuario = request.user.first_name 
    proceso = "Sale del Sistema"        
    descripcion = "El usuario salio de la aplicación."
    observaciones = "Salida del Sistema."
    modulo = "logout"
    VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)
    return redirect('login')



# carga el diseño del formulario 
from .forms import AsignaDeclaraciones, DeclaraForm
# paginacion 
from django.core.paginator import Paginator
 
from django.db.models import Exists,OuterRef,Subquery

# vista de inicio 
def inicio(request):
    return HttpResponse("<h1>Bienvenido</h1>")

# vista base 
def base(request):
    return render(request,'paginas/base.html')

# vista Clientes
def clientes(request):
    return render(request,'paginas/clientes.html')
# vista nosotros
def nosotros(request):
    return render(request, 'paginas/nosotros.html')


# vista visor
def visor(request):
    datos_decla = declaracion.objects.all().order_by('codigo')  
    # es el listado general y la cantidad por pagina 
    paginator = Paginator(datos_decla,8)            
    # crear variable page si no existe se pone 1
    pagina = request.GET.get("page") or 1   
    # el posts es la vista como tal de datos_decla a posts que es igual a publicaciones por pagina  
    posts   = paginator.get_page(pagina) 
    # se hace para saber la cantidad de paginas variable 
    pagina_actual  = int(pagina)
    # se define la cantidad de paginas con range en la variable paginas inicia en 1  
    paginas = range(1,posts.paginator.num_pages + 1)    
   # Paginacion se ve la cantidad de objetos en lista  
    return render(request, 'formas/visor.html', {'dvisor': posts,"paginas":paginas,"pagina_actual":pagina_actual})
    

# vista Crear 
def crear(request):
    dato_formulario = DeclaraForm(request.POST or None, request.FILES or None)
    if dato_formulario.is_valid():         
        dato_formulario.save()                                  
        messages.success(request,'Creado Correctamente')
        
        #registro de salida a bitacora 
        datos = dato_formulario.cleaned_data # obtiene datos del form 
        vdetalle =  datos.get('detalle')
        
        usuario = request.user.first_name 
        proceso = "Crea una nueva Declaración al Sistema"        
        descripcion = "Se Creo el registro "+ vdetalle
        observaciones = "Creacion de Registros."
        modulo = "Declaracion - Visor"
        VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)
        
        return redirect('visor')      
    
    return render(request,'formas/crear.html', {'var_formulario': dato_formulario })   

# vista Editar 
def editar(request, IDD):
    decla = declaracion.objects.get(IDDeclaracion = IDD)
    dato_formulario = DeclaraForm(request.POST or None, request.FILES or None, instance = decla )
    if dato_formulario.is_valid() and request.POST: 
        dato_formulario.save()
        messages.success(request,'Modificado Correctamente')
        
        # registro de bitacora
        usuario = request.user.first_name 
        proceso = "Realiza cambios a las Declaraciones."        
        descripcion = "Se ha modificado el registro  "+ decla.detalle
        observaciones = "Modificación de Registros."
        modulo = "Declaracion - Visor"
        VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)
        return redirect('visor')
    return render(request,'formas/editar.html',{'var_formulario': dato_formulario})

# Vista Eliminar
def elimina(request,IDD):
    decla= declaracion.objects.get(IDDeclaracion=IDD)
    decla.delete()  
    
    # registro de bitacora     
    usuario = request.user.first_name 
    proceso = "Elimina Declaraciones."        
    descripcion = "Ha sido eliminado el registro "+ decla.detalle
    observaciones = "Elimina Registros."
    modulo = "Declaracion - Visor"
    VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)  
    
    return redirect('visor')

# busca todos los clientes que no tenga asignada a un funcionario 
def pendientedeasignar(request):    
    clientes_pendientes = cliente_proveedor_cliente_proveedor.objects.annotate(
        tiene_asignacion=Exists(
            Asignacion.objects.filter(
                IDClientes_Proveedores=OuterRef('IDClientes_Proveedores')
                )
            )
        ).filter(tiene_asignacion=False,Estado = True)             
    return JsonResponse({'data': list(clientes_pendientes)})
  
        
# busca todos los clientes que no tenga asignada a un funcionario 
def pendiente(request):
    # clientes_pendientes = cliente_proveedor_cliente_proveedor.objects.all().order_by('Descripcion')  * todos
    # ids_asignacion = Asignacion.objects.values('IDClientes_Proveedores')
    # clientes_pendientes = cliente_proveedor_cliente_proveedor.objects.exclude(ID__in=Subquery(ids_asignacion))
    # busca los clientes que no tienen asignacion 
    clientes_pendientes = cliente_proveedor_cliente_proveedor.objects.annotate(
        tiene_asignacion=Exists(
            Asignacion.objects.filter(
                IDClientes_Proveedores=OuterRef('IDClientes_Proveedores')
                )
            )
        ).filter(tiene_asignacion=False,Estado = True,Tipo = True)             
    
    # es el listado general y la cantidad por pagina 
    paginator = Paginator(clientes_pendientes,8)  
              
    # crear variable page si no existe se pone 1
    pagina = request.GET.get("page") or 1   
    # el posts es la vista como tal de datos_decla a posts que es igual a publicaciones por pagina  
    posts   = paginator.get_page(pagina) 
    # se hace para saber la cantidad de paginas variable 
    pagina_actual  = int(pagina)
    # se define la cantidad de paginas con range en la variable paginas inicia en 1  
    paginas = range(1,posts.paginator.num_pages + 1)    
    # Paginacion se ve la cantidad de objetos en lista  
    return render(request, 'formas/pendientes.html', {'cvisor': posts,"paginas":paginas,"pagina_actual":pagina_actual})    

  
# asigna funcionarios 
def asigna(request):    
    datos_funcionario =planillas_planilla_funcionarios.objects.all().order_by('Nombre')  
    return render(request,'formas/asignacion.html',{'var_Funcionarios': datos_funcionario})        


# vista para traer todos los clientes 
def Clientes_General(request):
    todos_clientes=list(cliente_proveedor_cliente_proveedor.objects.values())     
    return JsonResponse({'data': list(todos_clientes)})
        
        
# vista para traer los clientes que aun no estan asignados 
def Clientes_pendientes(request):     
    clientes_pendientes = cliente_proveedor_cliente_proveedor.objects.annotate(
        tiene_asignacion=Exists(
            Asignacion.objects.filter(
                IDClientes_Proveedores=OuterRef('IDClientes_Proveedores')
                
                )
            )
        ).filter(tiene_asignacion=False,Estado = True,Tipo = True)
              
    return JsonResponse({'data':list(clientes_pendientes.values())}) 


# vista para buscar los clientes que tiene asignado el funcionario       
def Clientes_Funcionario(request,IDD):    
    clientes_funcionario = Asignacion.objects.filter(
        IDPlanilla_Funcionarios_id=IDD  # busca al funcionario
    ).annotate(
        tiene_asignacion=Exists(
            cliente_proveedor_cliente_proveedor.objects.filter(
                IDClientes_Proveedores=OuterRef('IDClientes_Proveedores_id')        
            )
        ),
        Descripcion=Subquery(
            cliente_proveedor_cliente_proveedor.objects.filter(
                IDClientes_Proveedores=OuterRef('IDClientes_Proveedores_id')                
            ).values('Descripcion')[:1]
        )
    )
        
    return JsonResponse({'data':list(clientes_funcionario.values())}) 

# es la vista para cargar las declaraciones que tiene asignadas cada cliente segun el funcionario 
def Declaracion_Cliente(request,IDD):
    declaraciones_asignadas = Asignacion.objects.filter(
        IDPlanilla_Funcionarios_id=IDD  # busca al funcionario
    ).select_related('IDDeclaracion')
        
    data = []  
    
    for asignacion in declaraciones_asignadas:
        data.append({
            'iddeclaracion':asignacion.IDDeclaracion.IDDeclaracion,
            'detalle':asignacion.IDDeclaracion.detalle,    
            'codigo':asignacion.IDDeclaracion.codigo,
            'tiempo':asignacion.IDDeclaracion.tiempo,
            'estado':asignacion.IDDeclaracion.estado,
            'presentada':asignacion.Fecha_Presenta,
            'asignada':asignacion.Fecha_Asigna,
        })
                                 
    return JsonResponse(data, safe=False)

# muestra todas las declaraciones que tiene el cliente asignadas 
def vsDeclaraciones_Cliente(request,IDD):
    declaraciones_asignadas = Asignacion.objects.filter(
        IDClientes_Proveedores=IDD  # busca al funcionario
    ).select_related('IDDeclaracion')
        
    data = []  
    
    for asignacion in declaraciones_asignadas:
        data.append({
            'iddeclaracion':asignacion.IDDeclaracion.IDDeclaracion,
            'detalle':asignacion.IDDeclaracion.detalle,    
            'codigo':asignacion.IDDeclaracion.codigo,
            'tiempo':asignacion.IDDeclaracion.tiempo,
            'estado':asignacion.IDDeclaracion.estado,
            'presentada':asignacion.Fecha_Presenta,
            'asignada':asignacion.Fecha_Asigna,
            'mes':asignacion.Mes,
        })
                                 
    return JsonResponse(data, safe=False)


# guarda los datos en la tabla asigna 
def Asigna_Declaracion(request,cliente_id,colaborador_id):
    # Obtener instancias de los modelos necesarios
    cliente = get_object_or_404(cliente_proveedor_cliente_proveedor, pk=cliente_id)
    colaborador = get_object_or_404(planillas_planilla_funcionarios, pk=colaborador_id)
    # crea un nuevo registro en la tabla asignacion 
    
    Asigna = Asignacion.objects.create(                                             
            Fecha_Asigna = date.today(),
            IDClientes_Proveedores_id = cliente_id,
            IDPlanilla_Funcionarios_id = colaborador_id,
            IDDeclaracion_id = 13,
            correo = 0     
            )
    # actualiza estado de clientes 
    cliente.Estado = False
    cliente.save()
        
   # Envía una respuesta JSON indicando éxito
    return JsonResponse({'success': True})

# esta funcion cargo los provee
def Asigna_Declaracion_Clientes(request):
    todos_clientes = cliente_proveedor_cliente_proveedor.objects.all().order_by('Descripcion')  
    return render(request,'formas/declaracion_clientes.html',{'data':todos_clientes})    

# esta funcion solo carga la pagina declaracion_clientes
def VsListaclientes(request):     
   #return JsonResponse({'success': True})   
   return render(request,'formas/declaracion_clientes.html') 

# muestra todos los cliente en el combo donde su estado este true 
def VsListaclientesdatosa(request):
    try:
        todos_clientes = cliente_proveedor_cliente_proveedor.objects.filter(Estado=True, Tipo=True).order_by('Descripcion').values()
        return JsonResponse({'data': list(todos_clientes)})
    except Exception as e:
        return JsonResponse({'error': 'Error al obtener los datos de clientes'}, status=500) 

# debe de mostrar los clientes que no tienen asignada una declaracion 
def VsClientessindeclaraciones(request):     
    clientes_sin_declaraciones = cliente_proveedor_cliente_proveedor.objects.annotate(
        tiene_asignacion=Exists(
            Declaracion_Clientes.objects.filter(
                IDClientes_Proveedores=OuterRef('IDClientes_Proveedores')
                )
            )
        ).filter(tiene_asignacion=False,Estado = True,Tipo = True).order_by('Descripcion')
              
    return JsonResponse({'data':list(clientes_sin_declaraciones.values())}) 

# debe de mostrar solo las declaraciones asignadas al cliente 
def VDeclaracion_Cliente_asignacion(request,IDD):    
    declaraciones_asignadas = Declaracion_Clientes.objects.filter(
        IDClientes_Proveedores_id=IDD  # busca al Cliente
    ).select_related('IDDeclaracion')
    
    data = []  
    
    for declarac in declaraciones_asignadas:
        data.append({
            'iddeclaracion_clientes':declarac.IDDeclaracion_Clientes,
            'codigo':declarac.IDDeclaracion.codigo,
            'detalle':declarac.IDDeclaracion.detalle,
            'fecha':declarac.Fecha_Asigna,    
            'estado':declarac.Estado,
            'tiempo':declarac.Observacion,            
        })                     
    return JsonResponse(data, safe=False)

# Vista Elimina la declaracion del cliente 
def velimina_declaracion_cliente(request,IDD):
    decla= Declaracion_Clientes.objects.get(IDDeclaracion_Clientes=IDD)
    IDDecla = decla.IDDeclaracion
    IDClien = decla.IDClientes_Proveedores
     
    
    #registro de salida a bitacora 
    usuario = request.user.first_name 
    proceso = "Desasigna Declaración"        
    descripcion = f"Se le quita la declaración {IDDecla} al Cliente {IDClien}."
    observaciones = "Elimina Declaracion."
    modulo = "Clientes"
    VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)   
    
    decla.delete()    
   # return JsonResponse({'success': True})
    return redirect('clientes_declaraciones')

# busca las declaraciones que no tiene asignado el cliente 
def vdeclaraciones_sin_asignar_al_cliente(request, IDD):
    # Obtener todas las declaraciones que no están asignadas al cliente
    declaraciones_no_asignadas = declaracion.objects.exclude(
        declaracion_clientes__IDClientes_Proveedores_id=IDD
    ).order_by('codigo').values()
    
    return JsonResponse(list(declaraciones_no_asignadas), safe=False)

# esta vista agrega nuevas declaraciones al cliente 
def vagregarunadeclaracion(request):
    if request.method == 'POST':
        data = json.loads(request.body)                                
        cliente_id = data.get('clienteID', None)
        declaracion_id = data.get('declaracionID', None)                                
        
        if cliente_id is None or declaracion_id is None:
            return JsonResponse({'error': 'IDs de cliente o declaración faltantes'}, status=400)

        try:
            fecha_asigna = datetime.strptime(data['Fecha_Asigna'], '%d/%m/%Y').strftime('%Y-%m-%d')
            
            nueva_declaracion_cliente = Declaracion_Clientes.objects.create(
                Fecha_Asigna=fecha_asigna,
                Estado=data['Estado'],
                Observacion=data['Observacion'],
                IDClientes_Proveedores_id=cliente_id,
                IDDeclaracion_id=declaracion_id,
            )            
            # obtiene el nombre del cliente 
            cliente_obj = cliente_proveedor_cliente_proveedor.objects.get(IDClientes_Proveedores = cliente_id  )
            Ncliente = cliente_obj.Descripcion
            # obtener el codigo y nombre de la declaracion 
            declaracion_obj =  declaracion.objects.get(IDDeclaracion = declaracion_id )
            Cdec = declaracion_obj.codigo
            Ndec = declaracion_obj.detalle 


            #registro de salida a bitacora 
            usuario = request.user.first_name 
            proceso = "Asignación de Declaración"        
            descripcion = f"Se le asigna la declaración {Cdec +' '+ Ndec} al cliente {Ncliente}."
            observaciones = "Asignacion de declaracion."
            modulo = "Clientes"
            VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)
                                    
            return JsonResponse({'message': 'Declaración de cliente creada correctamente'}, status=201)
        except Exception as e:
            print('Error al crear la declaración de cliente:', str(e))
            return JsonResponse({'error': 'Error al crear la declaración de cliente'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
# asigna las declaraciones al funcionario 
def clienteafuncionario(request):    
    if request.method == 'POST':  
        try:                          
            data = json.loads(request.body)                                   
            clientepend_id = data.get('IDClientes_Proveedores', None) 
            
            # Validar la presencia de datos importantes
            if 'IDClientes_Proveedores' not in data or 'IDPlanilla_Funcionarios' not in data or 'Fecha_Asigna' not in data:
                return JsonResponse({'error': 'Campos requeridos faltantes'}, status=400)
            
            #clientepend_id  = list(cliente_proveedor_cliente_proveedor.objects.values().filter(Tipo=True).order_by('Descripcion')             
            #clientepend_id=list(cliente_proveedor_cliente_proveedor.objects.values().filter(estado=True).order_by('codigo'))                       

            cliente_proveedor_instance = cliente_proveedor_cliente_proveedor.objects.filter(Tipo=1).get(pk=clientepend_id)                                      
            
            funcionario_id = data.get('IDPlanilla_Funcionarios', None)
            print('funcionario ',funcionario_id)
            
            funcionario_instance = planillas_planilla_funcionarios.objects.get(pk=funcionario_id) 
             
           
            if clientepend_id is None or funcionario_id is None:
                return JsonResponse({'error': 'IDs de cliente o funcionario faltantes'}, status=400)

            fecha = datetime.strptime(data['Fecha_Asigna'], '%d/%m/%Y').strftime('%Y-%m-%d')
                    
            # Obtener todas las declaraciones del cliente cliente_proveedor_instance
            #print("Cliente instancia",cliente_proveedor_instance)
            
            #Declaraciones_cliente = Declaracion_Clientes.objects.values().filter(IDClientes_Proveedores=clientepend_id)
            declaraciones_cliente = Declaracion_Clientes.objects.filter(IDClientes_Proveedores=clientepend_id)
                        
            # Crear las asignaciones con las declaraciones del cliente
            for declaracion in declaraciones_cliente:
            
                Asignacion.objects.create(
                    Fecha_Presenta=fecha,
                    Fecha_Asigna=fecha,
                    Fecha_Proxima=fecha,
                    correo=False,
                    IDClientes_Proveedores=cliente_proveedor_instance,
                    IDPlanilla_Funcionarios=funcionario_instance,
                    IDDeclaracion=declaracion.IDDeclaracion,
                )  
            
            # registro de bitacora     
            usuario = request.user.first_name 
            proceso = "Agrega Cliente a Funcionario."        
            descripcion = f"El usuario agrego el cliente '{cliente_proveedor_instance.Descripcion}' al funcionario   '{funcionario_instance.Nombre}' "
            observaciones = "Asigna Cliente a funcionario."
            modulo = "Asignación de Clientes"
            VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo) 
            
            return JsonResponse({'message': 'Asignacion a funcionario creada correctamente'}, status=201)
        except KeyError as e:
            return JsonResponse({'error': f'Campo requerido faltante: {e}'}, status=400)
        
        except cliente_proveedor_cliente_proveedor.DoesNotExist:
            return JsonResponse({'error': 'Cliente  no encontrado'}, status=404)
        
        except planillas_planilla_funcionarios.DoesNotExist:
            return JsonResponse({'error': 'Funcionario no encontrado'}, status=404)
        
        except Exception as e:
            print('Error al crear la asignación a funcionario:', str(e))
            return JsonResponse({'error': 'Error interno al procesar la solicitud'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    


# desasigna cliente a funcionario  quita los clientes a un funcionario  
def vsdesasignaclienteafuncionario(request, IDD):    
    try:                
        # asignación por IDClientes_Proveedores al funcionario 
        asignacion = Asignacion.objects.filter(IDClientes_Proveedores=IDD)                        
        #fun_id = asignacion.IDPlanilla_Funcionarios
        
        # busca funcionario 
        #busca_funcionario = planillas_planilla_funcionarios.objects.get(pk=fun_id)        
        #print(f'funcionario',{busca_funcionario})
        
        # busca cliente 
        cliente_proveedor_instance = cliente_proveedor_cliente_proveedor.objects.get(pk=IDD)                     
   
        # Elimina la asignación encontrada
        asignacion.delete()        
        
        # registro de bitacora     
        usuario = request.user.first_name 
        proceso = "Desasignación del Cliente al Funcionario."        
        descripcion = f"El usuario quitó  el cliente '{cliente_proveedor_instance.Descripcion}' al funcionario.  " 
        observaciones = "Desasignación del Cliente al funcionario."
        modulo = "Asignacion de Clientes"
        VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)             
        print("Bitácora registrada con éxito")
        
        # Devuelve una respuesta JSON de éxito
        return JsonResponse({'success': True})
    
    except ObjectDoesNotExist:
        # Si no se encuentra la asignación, devuelve un error 404
        return JsonResponse({'error': 'La asignación no existe'}, status=404)
    
    except Exception as e:
        # Para otros errores, devuelve un error 500 junto con el mensaje de error
        return JsonResponse({'error': str(e)}, status=500)
   

  
# abre el formulario de busqueda de declaracion 
def vbuscadeclaracion(request):
    return render(request,'formas/Busca_Declaracion_Clientes.html')

# abre el formulario de busqueda de declaracion --- revisar muestra todas las declaraciones -- 
def vbuscadeclaraciondatos(request):
    todas_declaraciones=list(declaracion.objects.values().filter(estado=True).order_by('codigo'))       
    return JsonResponse({'ldeclaraciones': list(todas_declaraciones)})  

# busca declaraciones asociadas a un cliente 
def vbuscadeclaraciondatosclientes(request,IDD):    
    declaraciones_asignadas = Declaracion_Clientes.objects.filter(
    IDDeclaracion=IDD  # busca declaraciones 
    ).select_related('IDClientes_Proveedores').values('IDClientes_Proveedores', 'IDClientes_Proveedores__IDClientes_Proveedores', 'IDClientes_Proveedores__Descripcion','IDClientes_Proveedores__Fecha_Ult_Movimiento','IDClientes_Proveedores__Estado')       
           
    return JsonResponse({'data': list(declaraciones_asignadas)})  
    
# activa la pantalla de activacion 
def viniciadeclaracion(request): 
    return render(request,'formas/inicia_Declaracion.html')    

#lista de funcionarios 
def vsfuncionarios(request):    
    datos_funcionario =list(planillas_planilla_funcionarios.objects.values().order_by('Nombre'))    
    return JsonResponse({'datafuncionario': list(datos_funcionario) })  
           
# busca las declaraciones que tiene asignada un cliente segun el funcionario ´prefetch_related()´
def vsfuncionarioinicia(request,idd2,idd):  
    declaraciones_cliente =Asignacion.objects.filter(
        IDClientes_Proveedores = idd2, 
        IDPlanilla_Funcionarios = idd
    ).select_related('IDDeclaracion')            

    datadeclaracion =list(declaraciones_cliente.values(
         'IDAsignacion',  
         'IDDeclaracion__codigo',  
         'IDDeclaracion__detalle', 
         'Fecha_Presenta',           
         'Fecha_Asigna', 
         'IDDeclaracion__tiempo',
         'IDPlanilla_Funcionarios',  
         'IDDeclaracion__estado',                         
         'correo', 
         'IDAsignacion',                   
         'Fecha_Proxima',
         'Iniciada',
         'Suspendida',
         'Rectificativa',
         'Mes',
    ))
    
    return JsonResponse(datadeclaracion, safe =False) 

# actualiza los campos de la tabla       
def vsActivaDeclaracion(request, idd):                
    if request.method=='POST':                     
       try:            
                             
            asignacion = Asignacion.objects.filter(pk=idd).first()   
                                                                                            
            if not asignacion:
                return JsonResponse({'success':False,'error': 'Asignacion no encotrada'})
        
            idcliente = asignacion.IDClientes_Proveedores                                   

            declaracion_obj = declaracion.objects.filter(IDDeclaracion=asignacion.IDDeclaracion.IDDeclaracion).first()      
            if not declaracion_obj:    
                return JsonResponse({'success': False,'error': 'Declaracion no encotrada '})
         
            # datos recibidos 
            data =json.loads(request.body.decode('utf-8'))                                 
            rectifica = data.get('rectificativa')     # marca del check                                                                      
            # actualiza campos             
            asignacion.Iniciada = True
            asignacion.Fecha_Asigna = date.today()               
            
            # el campo viene en on o en off
            if rectifica == 'on':
                asignacion.Rectificativa = True 
            elif rectifica =='off' or rectifica is None:
                asignacion.Rectificativa = False 
                asignacion.Fecha_Proxima = asignacion.Fecha_Presenta + timedelta(days=int(declaracion_obj.tiempo))
                
            # Guarda los campos
            asignacion.save()
            #historico_declaraciones.save()
            #print(f'Asignación actualizada: {asignacion}')  # Mensaje de depuración    
            
            #registro de ingreso a bitacora 
            usuario = request.user.first_name
            proceso = "Inicia Declaración"        
            descripcion = f"Se inicia declaración {declaracion_obj.codigo} {declaracion_obj.detalle} del Cliente {idcliente} referencia {asignacion.Fecha_Presenta}, Fecha asignada {asignacion.Fecha_Asigna}, Mes proceso {asignacion.Mes} rectificativa {rectifica}"
            observaciones = f"Se procede al inicio de la declaracion '{rectifica}'"
            modulo = "Inicia Declaración"
            VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)
            
            return JsonResponse({'success':True})        
       except Exception as e:
            return JsonResponse({'success': False,'error': str(e)})         
    else:
           return JsonResponse({'success': False,'error': 'No se Guardaron los datos'})         



# actualiza los campos de la tabla para cerrar la declaracion 
def vsCierraDeclaracion(request, idd): 
    if request.method == 'GET':            
        try:            
                  
            asignacion = Asignacion.objects.filter(pk=idd).first()  
            declaracion_obj = declaracion.objects.filter(IDDeclaracion=asignacion.IDDeclaracion.IDDeclaracion).first()                              
            
            idcliente = asignacion.IDClientes_Proveedores              
            
            
            if declaracion_obj:         
                
                # Crear registro en Historico_Declaraciones
                Historico_Declaraciones.objects.create(                                             
                    IDAsignacion=idd,
                    Fecha_Presenta=asignacion.Fecha_Presenta,
                    Fecha_Asigna=asignacion.Fecha_Asigna,
                    Fecha_Proxima=asignacion.Fecha_Proxima,
                    Fecha_Cierre=date.today(),
                    correo=False,
                    Iniciada=asignacion.Iniciada,
                    Suspendida=asignacion.Suspendida,
                    Usuario_Cierre='S/A',  
                    Numero_Comprobante='',
                    Fecha_Final=None,
                    IDClientes_Proveedores=asignacion.IDClientes_Proveedores,
                    IDPlanilla_Funcionarios=asignacion.IDPlanilla_Funcionarios,
                    IDDeclaracion=asignacion.IDDeclaracion,
                    rectificativa = asignacion.Rectificativa,
                    Mes = asignacion.Mes
                )
                
                # Actualizar campos en Asignacion ajusta la fecha y valida mes 
                asignacion.Iniciada = False
                asignacion.Suspendida = False
                
                
                if not asignacion.Rectificativa:
                    asignacion.Fecha_Presenta = asignacion.Fecha_Proxima
                    mes = asignacion.Mes + 1                     
                    if mes >12:
                        mes = 1
                        
                    asignacion.Mes = mes 
                                        
                asignacion.Rectificativa  = False     
                # Guardar cambios en Asignacion
                asignacion.save()
                
                #registro de ingreso a bitacora 
                usuario = request.user.first_name
                proceso = "Cierre de Declaración"        
                descripcion = f"Se cierra declaración {declaracion_obj.codigo} {declaracion_obj.detalle} del Cliente {idcliente} referencia {asignacion.Fecha_Presenta}, Fecha asignada {asignacion.Fecha_Asigna}, Mes proceso {mes -1}"
                observaciones = f"Se procede al cierre de la  declaración "
                modulo = "Cierre Declaración"
                VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)
                
                
                                
                return JsonResponse({'success': True})
        except Exception as e:        
            return JsonResponse({'success': False, 'error': str(e)})         
    else:         
        return JsonResponse({'success': False, 'error': 'No se Guardaron los datos'})
       

# suspende declaracion 
def vsSuspendeDeclaracion(request,idd):     
 if request.method=='GET':             
    try:                      
        asignacion = Asignacion.objects.filter(pk=idd).first()  
        
        idcliente = asignacion.IDClientes_Proveedores  
                  
        declaracion_obj = declaracion.objects.filter(IDDeclaracion=asignacion.IDDeclaracion.IDDeclaracion).first()                  
        if declaracion_obj:                        
         # actualiza campos         
         asignacion.Suspendida = True             
         # Guarda los campos                
         asignacion.save()   
         
        #registro de ingreso a bitacora 
        usuario = request.user.first_name
        proceso = "Suspende Declaración"        
        descripcion = f"Se suspende declaración {declaracion_obj.codigo} {declaracion_obj.detalle} del Cliente {idcliente} referencia {asignacion.Fecha_Presenta}, Fecha asignada {asignacion.Fecha_Asigna}, Mes proceso {asignacion.Mes}"
        observaciones = f"Se procede al suspender la  declaración "
        modulo = "Suspende Declaración"
        VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)     
        
        return JsonResponse({'success':True})
    except Exception as e:        
        return JsonResponse({'success': False,'error': str(e)})         
 else:    
        return JsonResponse({'success': False,'error': 'No se Guardaron los datos'})   
       

# ve el Status de las declaraciones       
def VstatusDeclaracion(request):       
     # apertura el formulario de Visor de Status 
    return render(request, 'formas/Status.html')


# Ver Status de Declaracion - muestra todos los datos de las declaraciones  
def VsEstatusDeclaracion(request): 
    Total_Declaraciones = Asignacion.objects.select_related(
        'IDClientes_Proveedores', 
        'IDPlanilla_Funcionarios', 
        'IDDeclaracion'
    ).all().order_by("Fecha_Presenta")
    
    datadeclaracion = list(Total_Declaraciones.values(
        'IDDeclaracion',  # Acceder al ID de la declaración relacionada
        'IDDeclaracion__codigo',
        'IDDeclaracion__detalle',
        'Fecha_Asigna',
        'Fecha_Presenta',
        'IDPlanilla_Funcionarios__Nombre',  # Acceder al nombre del funcionario
        'IDDeclaracion__estado',
        'Iniciada',
        'Suspendida'
    ))

    return JsonResponse(datadeclaracion, safe=False)


# ver la condicion global de las declaraciones actuales mas detallado  --- vision global 
def VsVisionDeclaracion(request):
    Total_Declaraciones = Asignacion.objects.select_related(
        'IDClientes_Proveedores', 
        'IDPlanilla_Funcionarios', 
        'IDDeclaracion'
    ).all().order_by("Fecha_Presenta")
    
    datadeclaracion = list(Total_Declaraciones.values(
        'IDDeclaracion',  # Acceder al ID de la declaración relacionada
        'IDDeclaracion__codigo',
        'IDDeclaracion__detalle',
        'Fecha_Asigna',
        'Fecha_Presenta',
        'IDPlanilla_Funcionarios__Nombre',  # Acceder al nombre del funcionario
        'IDDeclaracion__tiempo',
        'IDDeclaracion__estado', 
        'IDDeclaracion__observaciones',
        'Iniciada',
        'Suspendida',
        'IDClientes_Proveedores__IDClientes_Proveedores',
        'IDClientes_Proveedores__Descripcion',
        'IDClientes_Proveedores__Email',
    ))

    return render(request,'formas/Vision_Global_Declaraciones.html',{'v_Global': datadeclaracion  })    
    


# suspende las declaraciones que el funcionario esta trabajando 
def VsActivaSuspendida(request,idd):
    if request.method=='GET':
       try:      
         asignacion = Asignacion.objects.filter(pk=idd).first()   
         idcliente = asignacion.IDClientes_Proveedores                                                 
         declaracion_obj = declaracion.objects.filter(IDDeclaracion=asignacion.IDDeclaracion.IDDeclaracion).first()                          
                     
         if declaracion_obj:                                                   
            # actualiza campos 
            asignacion.Suspendida = False                         
            # Guarda los campos
            asignacion.save()
            
            
            #registro de ingreso a bitacora 
            usuario = request.user.first_name
            proceso = "Reinicia Declaración"        
            descripcion = f"Se reincia declaración {declaracion_obj.codigo} {declaracion_obj.detalle} del Cliente {idcliente} referencia {asignacion.Fecha_Presenta}, Fecha asignada {asignacion.Fecha_Asigna}, Mes proceso {asignacion.Mes}"
            observaciones = f"Se procede al reiniciar la  declaración "
            modulo = "Reinicio Declaración"
            VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)     
            return JsonResponse({'success':True})
         else:
             return JsonResponse({'success': False, 'error': 'No se encontró ninguna declaración relacionada'}) 
       except Exception as e:
           return JsonResponse({'success': False,'error': str(e)})         
    else:
           return JsonResponse({'success': False,'error': 'No se Guardaron los datos'})  
       
# carga el calendario tributario        
def VsCalendario(request): 
    return render(request,'formas/calendario.html')    

# carga el confirmador de declaraciones
def VsConfirmaDeclaracion(request): 
    return render(request,'formas/Confirma_Declaraciones.html')    

# Ver Status de Declaracion - muestra todos los datos de las declaraciones filtra si el numero de comprobante
# es vacio o nulo
def VsEstatusDeclaracionHistoricas(request): 
    Total_Declaraciones = Historico_Declaraciones.objects.select_related(
        'IDClientes_Proveedores', 
        'IDPlanilla_Funcionarios', 
        'IDDeclaracion'
    ).filter(
        Q(Numero_Comprobante__isnull=True) | Q(Numero_Comprobante='')
    ).order_by("Fecha_Cierre")             
    
    datadeclaracion = list(Total_Declaraciones.values(
        'IDHistorico_Declaraciones',  # Acceder al ID de la declaración relacionada
        'IDDeclaracion__codigo',
        'IDDeclaracion__detalle',
        'IDClientes_Proveedores__IDClientes_Proveedores',
        'IDClientes_Proveedores__Descripcion',
        'Fecha_Asigna',
        'Fecha_Presenta',
        'Fecha_Cierre',
        'IDPlanilla_Funcionarios__Nombre',  # Acceder al nombre del funcionario
        'rectificativa'                
    ))

    
    return JsonResponse(datadeclaracion, safe=False)

# ajuste a vista con calendarios 

def VsConfirma_malo(request, idd):     
    if request.method == 'POST':
        try:
            # Obtiene el objeto historico
            historico_declaracion = Historico_Declaraciones.objects.get(pk=idd)
            idc = historico_declaracion.IDDeclaracion 
            chisto = historico_declaracion.objects.all()
            print('histo',chisto)
            # Obtiene los datos recibidos en el json
            data = json.loads(request.body.decode('utf-8'))
            
            # Extrae datos
            numero_comprobante = data.get('numero_comprobante')
            fecha_cierre = parse_date(data.get('fecha_cierre'))
            correo = data.get('correo') 
            
            
            print('datos   idc',idc)
                                                                           
            # Actualiza campos en el objeto historico_declaracion
            historico_declaracion.Numero_Comprobante = numero_comprobante
            historico_declaracion.Fecha_Final = fecha_cierre
            historico_declaracion.correo = correo == 'Si'
            
            # Extrae la fecha_presenta del objeto historico_declaracion
            fecha_presenta = historico_declaracion.Fecha_Presenta
                                            
            if fecha_presenta:               
                # Extrae el mes y el año de la fecha_presenta
                mes_grid = fecha_presenta.month
                anio_grid = fecha_presenta.year               
                                                                  
                # calendario = calendario_tributario.objects.all()  # Obtiene todos los registros
                #print('todos',calendario)
                                                                
                print("fecha",mes_grid,anio_grid,idc)                  
                                                
                # Buscar el calendario tributario usando filtros
                calendario = calendario_tributario.objects.filter(
                    ID = idc,
                    Fecha_Presenta__month = mes_grid, 
                    Fecha_Presenta__year = anio_grid                                                                     
                ).first()  # primer registro 
                
                print('calendario total',calendario)
                                
                #iddeclaracion = iddeclaracionb                                
                if calendario:
                    # Si tiene algo lo actualiza                                                             
                    historico_declaracion.IDCalendario_tributario = calendario.IDDeclaracion
                    
            else:
                return JsonResponse({'success': False, 'error': 'El campo fecha_presenta está vacío en el registro de declaraciones.'})
            
            # Guarda los cambios en la base de datos
            historico_declaracion.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo POST'})



# Confirma las declaraciones cerradas y presentadas para archivo          
def VsConfirma(request, idd):     
    if request.method == 'POST':
        try:
            # se obtiene el objeto historico 
            historico_declaracion = Historico_Declaraciones.objects.get(pk=idd)
            # ver los datos recibidos en el json 
            data =json.loads(request.body.decode('utf-8'))
            #print('datos recibido',data )            
            # se obtienen los datos                                
            correo = data.get('correo')           
                        
            # Actualizar los campos en el objeto historico_declaracion
            historico_declaracion.Numero_Comprobante = data.get('numero_comprobante')  
            historico_declaracion.Fecha_Final = data.get('fecha_cierre')
            historico_declaracion.correo = True if correo =='Si' else False                                        
            # Guardar los cambios en la base de datos
            historico_declaracion.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo POST'})

# levanta el formulario para la declaracion historico cerrada 
def VsDeclaracionesConfirmadasCerradas(request):       
        return render(request,'formas/Declaraciones_Confirmadas.html')   
    
# Muestra las declaraciones cerradas y archivadas     
def VsDeclaracionesConfirmadasCerradasAplicadas(request):        
    Total_Declaraciones = Historico_Declaraciones.objects.select_related(
        'IDClientes_Proveedores', 
        'IDPlanilla_Funcionarios', 
        'IDDeclaracion'
    ).filter(
        Q(Numero_Comprobante__isnull = False) & ~Q(Numero_Comprobante='')
    ).order_by("-Fecha_Cierre")
                   
    
    datadeclaracion = list(Total_Declaraciones.values(
        'IDHistorico_Declaraciones',  # Acceder al ID de la declaración relacionada
        'IDDeclaracion__codigo',
        'IDDeclaracion__detalle',
        'IDClientes_Proveedores__IDClientes_Proveedores',
        'IDClientes_Proveedores__Descripcion',
        'Fecha_Asigna',
        'Fecha_Presenta',
        'Fecha_Cierre',
        'IDPlanilla_Funcionarios__Nombre',  # Acceder al nombre del funcionario
        'IDDeclaracion__estado',
        'correo',
        'Numero_Comprobante',
        'Fecha_Final'                
    ))    
    return JsonResponse(datadeclaracion, safe=False)


# busca la fecha donde se quieren sacar las declaraciones 
def VsBuscaporfecha(request, fecha):
  
    try:                
        Total_Declaracion = calendario_tributario.objects.filter(Fecha_Presenta=fecha).order_by("-Fecha_Presenta")
        
        datadeclaracion = list(Total_Declaracion.values(
            'IDCalendario_tributario',            
            'IDDeclaracion__codigo',
            'IDDeclaracion__detalle',
            'IDDeclaracion__tiempo',
            'IDDeclaracion__observaciones'
        ))
     
        return JsonResponse(datadeclaracion, safe=False)
    
    except Exception as e:
        # Manejo genérico de errores, imprime el error en la consola del servidor
        print('Error en consulta:', e)
        return JsonResponse({'error': str(e)}, status=500)

# realiza la inclusion de la nueva declaracion al calendario de declaraciones     
def VsAgregaDeclaracionCalendario(request,fch):
    if request.method == 'POST':     
           
        data = json.loads(request.body.decode('utf-8')) 
        #print('Fecha recibida',fch,data)                                                                                                    
        #declaracion_obj = declaracion.objects.get(id=declaracion_id)        
        declaracion_id = data.get('IDDeclaracion', None)                 
        observaciones = data.get('Observaciones',None)                                   
        
        try:       
            # Verificar si existe una instancia válida de declaracion con el ID proporcionado            
            declaracion_instance = declaracion.objects.get(IDDeclaracion=declaracion_id)
            
            # Verificar si ya existe una entrada en calendario_tributario con esta declaración
            if calendario_tributario.objects.filter(
                IDDeclaracion=declaracion_instance,
                Fecha_Presenta = fch).exists():
                                
                return JsonResponse({'error': 'Esta declaración ya está incluida en el calendario'}, status=400)                      
                
            nueva_declaracion_calendario = calendario_tributario.objects.create(
                Fecha_Presenta=fch,                
                Observaciones=observaciones,
                IDDeclaracion=declaracion_instance,
            )     
            
            #registro de salida a bitacora 
            usuario = request.user.first_name 
            proceso = "Agrega Declaraciones al Calendario Tributario"        
            descripcion = "Se agrego la Declaracion "+ declaracion_instance.detalle + ' Fecha asignada : '+fch
            observaciones = "Ingreso al Calendario Tributario."
            modulo = "Calendarización"
            VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)                                      
            
            return JsonResponse({'message': 'Declaración incluida'}, status=201)
        except Exception as e:  
            print('Error:', str(e))          
            return JsonResponse({'error': 'Error al crear al asignar la declaración '}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
# elimina la declaracion del calendario tributario
def VsCalendario_Tributario_lineaBorra(request,linea):  
    try:                       
        decla= calendario_tributario.objects.get(IDCalendario_tributario=linea)    
        
        # Obtener el nombre del detalle de la declaración asociada
        detalle_declaracion = decla.IDDeclaracion.detalle
        
        decla.delete()  
        
        #registro de salida a bitacora 
        usuario = request.user.first_name 
        proceso = "Elimina Declaraciones al Calendario Tributario"        
        descripcion = f"Se eliminó la Declaración '{detalle_declaracion}' Fecha asignada: {decla.Fecha_Presenta}"
        observaciones = "Elimino la Declaracion del Calendario Tributario."
        modulo = "Calendarización"
        VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)  
        
        
        
        return JsonResponse({'message': 'Eliminado correctamente'}, status=200)
    except calendario_tributario.DoesNotExist:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)   
    
# levanta el formulario para el calendario tributario ve todo lo calendarizado por año y mes 
def VsCalendarioTributario(request):    
    return render(request,'formas/Calendario_Tributario.html')       
 
# busca las declaraciones del año solicitado 
def VsBuscadeclaracionxan(request, anSeleccionada):
   # an_Selecionado = int(anSeleccionada) # convierte el año        
    try:                  
        an = int(anSeleccionada) 
                                 
        Total_Declaraciones = calendario_tributario.objects.filter(Fecha_Presenta__year = an
        ).order_by("-Fecha_Presenta")  
                                      
        datadeclaracion = list(Total_Declaraciones.values(
            'IDCalendario_tributario',            
            'IDDeclaracion__codigo',
            'IDDeclaracion__detalle',
            'Fecha_Presenta'            
        ))
                  
        return JsonResponse(datadeclaracion, safe=False)        
                                        
    except calendario_tributario.DoesNotExist:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'El año proporcionado no es válido'}, status=400)
    except Exception as e:
        print(f"Error: {e}")  # Imprime el error en la consola
        return JsonResponse({'error': str(e)}, status=500)   
    

# busca las declaraciones del año solicitado 
def VsReasignadeclaracion(request):    
     return render(request,'formas/Calendario_Tributario_Reasigna.html')       
 
 
 # Muestra todos los movimientos 
def VsBitacora(request):
    # busca el usuario a ver si existe        
      if request.method == 'GET':         
            
            try:                                               
                # muestra los datos de parametros 
                Bitacoras = Bitacora.objects.all().order_by("-Fecha_Sistema") 
                 
                # convierte los datos en diccionario
                tbitacora = list(Bitacoras.values(     
                        'IDBitacora',
                        'Fecha_Sistema',
                        'Usuario',         
                        'Proceso',
                        'Descripcion',
                        'Observaciones',                        
                        'Modulo'
                    ))
                                                                                               
                return render(request,'formas/Bitacora.html',{'var_formulario': tbitacora}) 
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
      else:
            return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo GET'})
         

def VsCreaBitacora(request,Usr,Pro,Des,Obs,Modu):    
    # crea un salva nuevo registro en la tabla bitacora    
    Nbitacora = Bitacora.objects.create(                                                     
            Usuario = Usr,
            Proceso = Pro,
            Descripcion = Des,
            Observaciones = Obs,
            Modulo = Modu,
            )

    