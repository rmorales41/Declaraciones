from datetime import date
import json
from pyexpat.errors import messages
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect, render
from psutil import users
from django.contrib.auth.models import User
from django.contrib import messages


from libreria.forms import PermisoForm, RolesForm
from libreria.models import Asignacion, Bitacora, Parametros_Declaraciones, Permisos, Roles

# levanta pagina
def VsParametros(request):       
       return render(request,'formas/Parametros.html')
   
# muestra todas las asignaciones realizadas para que pueda ver el mes que esta en proceso 
def VsAjuste_Declaracion(request):
       try:
        # Obtener las asignaciones de todos los clientes esto va a permitir ajustar el mes que el sistema 
        # va controlando 
        asignaciones_lista = Asignacion.objects.filter(            
        ).values(
            'IDAsignacion',
            'IDClientes_Proveedores__Descripcion',
            'IDDeclaracion__codigo',
            'IDDeclaracion__detalle',
            'Mes',
            'Mes'
        ).order_by('Mes')

        # Convertir el queryset en una lista de diccionarios
        datos = list(asignaciones_lista)
        
        # Retornar los datos como JsonResponse
        return render(request,'formas/Ajuste_Declaraciones.html',{'var_asignaciones': datos}) 
       

       except Exception as e:
         error_msg = f"Error en la vista VsAjuste_Declaracion: {str(e)}"
         print(error_msg)  # Registrar el error en los registros de la aplicación
         return JsonResponse({'error': error_msg}, status=500)


# Permite confirmar el cambio de mes de las declaraciones asignadas del modelo de seguridad 
def VsConfirmaMes(request,idd):       
    if request.method == 'POST':   
        try:                               
            asignacion = Asignacion.objects.get(pk=idd)     # se obtiene el objeto de la tabla Asignacion             
            data =json.loads(request.body.decode('utf-8'))  # ver los datos recibidos en el json                                
            mescambio = data.get('mesdato')                 # se obtienen los datos                                                          
            asignacion.Mes = mescambio                      # Actualizar los campos de la tabla asignacion                           
            asignacion.save()                               # Guardar los cambios en la base de datos

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo POST'}) 
    

# muestra los datos de la linea de parametros 
def VsParametrosDatos(request):
   
    if request.method == 'GET':           
        try:                                               
                # muestra los datos de parametros 
                Total_parametro = Parametros_Declaraciones.objects.all()                                                                                                   
                tparametro = list(Total_parametro.values(     
                        'IDParametros_Declaraciones',
                        'Nombre',
                        'Ubicacion_logo',         
                        'Usuario',
                        'Clave',
                        'Nombre_Base',
                        'Puerto',
                        'Server',
                        'IDCia',    
                        'Ubicacion_logo',
                        'Calendario',
                    ))                                                                  
      
                if tparametro:
                        return JsonResponse(tparametro, safe=False)  # safe=False permite listas
                else:
                        return JsonResponse({'success': False, 'error': 'No se encontraron parámetros'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo GET'})
                
# Actualiza los datos del parametro 
def VsParametrosConfirma(request,IDreg):   
    if request.method == 'POST':   
        try:                               
            vparametros = Parametros_Declaraciones.objects.get(pk=IDreg)   
            data =json.loads(request.body.decode('utf-8'))  # ver los datos recibidos en el json                                
                              
            vnombre = data.get('nombre')                 # se obtienen los datos                                                          
            vbase = data.get('basedatos')
            vpuerto = data.get('puerto')
            vserver = data.get('server')
            vusuario = data.get('usuario')
            vclave = data.get('clave')
            vidc = data.get('idcia')
            vubicacion_logo = data.get('inputGroupFile04')
            vcalendario = data.get('calendario')
            
            vparametros.Nombre = vnombre                      # Actualizar los campos de la tabla asignacion                           
            vparametros.Nombre_Base = vbase
            vparametros.Puerto = vpuerto
            vparametros.Server = vserver
            vparametros.Usuario = vusuario
            vparametros.Clave = vclave
            vparametros.IDCia = vidc    
            vparametros.Calendario = vcalendario
            
             # Validar vubicacion_logo 
            if vubicacion_logo not in [None, '', 'None']:
                vparametros.Ubicacion_logo = vubicacion_logo            
                                      
            vparametros.save()                               # Guardar los cambios en la base de datos
            
            #return JsonResponse(vparametros, safe=False)  
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo POST'}) 
   
   
# registro de Usuarios del Sistema 
def VsRusuarios(request):   
        return render(request,'formas/Usuarios.html')

# Muestra todos los usuarios para verlos en la pantalla     
def VsBuscaUsuarios(request):       
       if request.method == 'GET':           
        try:                                               
                # muestra los datos de parametros 
                Total_usuarios = User.objects.all()                                                                                                   
                tusuarios = list(Total_usuarios.values(     
                        'id',
                        'username',
                        'first_name',         
                        'last_name',
                        'email',
                        'is_active',                        
                    ))                                                                                  
                if tusuarios:
                        return JsonResponse(tusuarios, safe=False)  
                else:
                        return JsonResponse({'success': False, 'error': 'No se encontraron los usuarios'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
       else:
            return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo GET'})


# Permite crear usuarios al sistema         
def VsCreaUsuarios(request):
    # busca el usuario a ver si existe         
        if request.method == 'POST':                           
         try:             
            vid = request.POST.get('idd')                                 
            vusuario = request.POST.get('usuario')
            vnombre = request.POST.get('nombre')
            vclave = request.POST.get('clave')
            vapellido = request.POST.get('apellido')
            vactivo = request.POST.get('activo')
            vemail = request.POST.get('email')            
            
            if not all([vusuario, vnombre, vclave, vapellido, vemail]):
                return JsonResponse({'success': False, 'error': 'Faltan campos requeridos'})
                        
       
            if vid:       
                try:
                   
                    usuario_existente  = User.objects.get(id=vid)
                    
                    usuario_existente.username = vusuario
                    usuario_existente.first_name = vnombre
                    usuario_existente.last_name = vapellido
                    usuario_existente.email = vemail
                    usuario_existente.is_active = vactivo                                    
                    
                    usuario_existente.save()
                except User.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'El usuario no existe'})  
            else:        
                # crear un nuevo usuario 
                if User.objects.filter(username=vusuario).exists():
                    return JsonResponse({'success': False, 'error': 'El nombre de usuario ya existe'})
                
                nuevo_usuario = User(
                    username = vusuario,
                    password = vclave,
                    first_name = vnombre,
                    last_name = vapellido,
                    is_active = vactivo ,
                    email = vemail, 
            )
            
                # Establecer la contraseña usando set_password para manejar el hashing
                nuevo_usuario.set_password(vclave) 
                nuevo_usuario.save()   # guarda el usuario                       
                        
             # Obtener datos actualizados para la tabla
            usuarios = User.objects.all().values('id', 'username', 'first_name', 'last_name', 'email', 'is_active')
            usuarios_lista = list(usuarios)
            
            return JsonResponse({'success': True, 'usuarios': usuarios_lista})
         except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        

# consulta de Usuarios 
def VsUsrBusca(request,IDD):    
    if request.method == 'GET':           
        try:         
            Busuario = User.objects.filter(id=IDD).values('id', 'username', 'first_name', 'last_name', 'email', 'is_active').first()                                                            
            if Busuario:
                    return JsonResponse({'success': True, 'usuario': Busuario}) 
            else:
                    return JsonResponse({'success': False, 'error': 'No se encontraron los usuarios'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
            return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo GET'})

# eliminar usuario 
def  VsEliminaUsuario(request,IDD):      
    if request.method == 'DELETE':
        try:
            usuario = User.objects.get(id=IDD)
            usuario.delete()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado'})
    else:
        return HttpResponseNotAllowed(['DELETE'])
    
    
    
# Roles 
def VsRoles(request):      
    try:
        Troles = Roles.objects.all()                                                                                                       
        ttroles = list(Troles.values(     
                        'IDRoles',
                        'Fecha_Sistema',
                        'Detalle',         
                        'Observaciones',                        
                    ))                                                                                     
        
        # Retornar los datos como JsonResponse
        return render(request,'formas/roles.html',{'var_roles': ttroles})       

    except Exception as e:
         error_msg = f"Error en la vista Roles: {str(e)}"
         print(error_msg)  # Registrar el error en los registros de la aplicación
    return JsonResponse({'error': error_msg}, status=500)
     
     
# Crear los roles      
def VsNuevo_Roles(request):
    dato_formulario = RolesForm(request.POST or None, request.FILES or None)
    if dato_formulario.is_valid():         
        dato_formulario.save()                                  
        messages.success(request,'Creado Correctamente')
        
        #registro de salida a bitacora 
        #datos = dato_formulario.cleaned_data # obtiene datos del form 
        #vdetalle =  datos.get('detalle')
        
        #usuario = request.user.first_name 
        #proceso = "Crea una nueva Declaración al Sistema"        
        #descripcion = "Se Creo el registro "+ vdetalle
        #observaciones = "Creacion de Registros."
        #modulo = "Declaracion - Visor"
        #VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)
        
        return redirect('Roles')      
    
    return render(request,'formas/Editar_Rol.html', {'var_formulario': dato_formulario })  


     
# Editar Roles 
def Editar_Rol(request, IDD):    
    Rol = Roles.objects.get(IDRoles = IDD)    
    dato_formulario = RolesForm(request.POST or None, request.FILES or None, instance = Rol )    
    if request.method == 'POST':
        if dato_formulario.is_valid():
            dato_formulario.save()
            messages.success(request,'Modificado Correctamente')
            return redirect('Roles')                   
                      
    #  return redirect('visor')
    return render(request,'formas/Editar_Rol.html',{'var_formulario': dato_formulario})

# eliminar Rol
def  VsBorrar_Rol(request,IDD):    
    
    if request.method == 'DELETE':
        print('id',IDD) 
        try:
            rol = Roles.objects.get(IDRoles=IDD)
            rol.delete()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Rol no encontrado'})
    else:
        return HttpResponseNotAllowed(['DELETE'])


# control de Permisos vista global   
def VsPermisos(request):
    try:
        Tpermisos = Permisos.objects.all()                                                                                                       
        ttpermisos = list(Tpermisos.values(     
                        'IDPermisos',
                        'Fecha_Sistema',
                        'Nombre_Permiso',         
                        'Formulario',                        
                        'Url',
                        'Observaciones',
                    ))                                                                                     
        
        # Retornar los datos como JsonResponse
        return render(request,'formas/permisos.html',{'var_permisos': ttpermisos})       

    except Exception as e:
         error_msg = f"Error en la vista Permisos: {str(e)}"
         print(error_msg)  # Registrar el error en los registros de la aplicación
    return JsonResponse({'error': error_msg}, status=500)

     
# Nuevo Permiso       
def VsNuevo_Permiso(request):
    dato_formulario = PermisoForm(request.POST or None, request.FILES or None)
    
    if dato_formulario.is_valid():         
        dato_formulario.save()                                  
        messages.success(request,'Creado Correctamente')
        
        #registro de salida a bitacora 
        #datos = dato_formulario.cleaned_data # obtiene datos del form 
        #vdetalle =  datos.get('detalle')
        
        #usuario = request.user.first_name 
        #proceso = "Crea una nueva Declaración al Sistema"        
        #descripcion = "Se Creo el registro "+ vdetalle
        #observaciones = "Creacion de Registros."
        #modulo = "Declaracion - Visor"
        #VsCreaBitacora(request, usuario, proceso, descripcion, observaciones, modulo)
        
        return redirect('Permisos')      
    
    return render(request,'formas/Crear_Permiso.html', {'var_formulario': dato_formulario }) 
      

# Editar Permiso 
def VsEditar_Permiso(request,IDD):
    try:
        Tpermsios = Permisos.objects.get(IDPermisos = IDD)            
        dato_formulario = PermisoForm(request.POST or None, request.FILES or None, instance = Tpermsios )    
        if request.method == 'POST':
            if dato_formulario.is_valid():
                dato_formulario.save()
                messages.success(request,'Modificado Correctamente')
                return redirect('Permisos')                   
                      
        #  return redirect('visor')
        return render(request,'formas/Editar_Permiso.html',{'var_formulario': dato_formulario})    

    except Exception as e:
         error_msg = f"Error en la vista Permisos: {str(e)}"
         print(error_msg)  # Registrar el error en los registros de la aplicación
    return JsonResponse({'error': error_msg}, status=500)



# Asigna Roles  
def VsAsigna_Rol(request):
    try:
        Troles = Roles.objects.all()                                                                                                       
        ttroles = list(Troles.values(     
                        'IDRoles',
                        'Fecha_Sistema',
                        'Detalle',         
                        'Observaciones',                        
                    ))                                                                                     
        
        # Retornar los datos como JsonResponse
        return render(request,'formas/Asigna_Rol.html',{'var_roles': ttroles})       

    except Exception as e:
         error_msg = f"Error en la vista Roles: {str(e)}"
         print(error_msg)  # Registrar el error en los registros de la aplicación
    return JsonResponse({'error': error_msg}, status=500)



# lista general de permisos 
def VsAsigna_GRol(request):      
    try:
        Tpermisos = Permisos.objects.all()                                                                                                       
        ttpermisos = list(Tpermisos.values(     
                        'IDPermisos',
                        'Nombre_Permiso',                        
                    ))                                                                                     
        
        # Retornar los datos como JsonResponse
        return JsonResponse({'success':True,'permisos': ttpermisos})       
    

    except Exception as e:
         error_msg = f"Error en la vista Roles: {str(e)}"
         print(error_msg)  # Registrar el error en los registros de la aplicación
    return JsonResponse({'error': error_msg}, status=500)