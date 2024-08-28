from django.urls import path

from . import views
from .Vistas import Views_BuscaDeclaracionxm,Views_pendiente_realizar,Views_Historico_Movimientos,Views_Funcionarios
from .Vistas import Views_Historico_Movimientos_Busqueda,Views_Beneficios,Views_Utilitarios,Views_ReportesGenerales

from .Vistas import Views_Statttus 

 
# asi con estos dos se maneja eel inventario
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.auth import views as auth_views

urlpatterns = [
     
    # menu principal   
    path('',views.login_view, name = 'login'),      
    path('logout/',views.logout_view, name = 'login'),      
    path('base',views.base, name= 'base'),
        
    
    # Menu de Declaraciones     
    path('visor/',views.visor,name='visor'),
    path('crear',views.crear,name='crear'),
    path('editar/<int:IDD>',views.editar,name='editar'),
    path('elimina/<int:IDD>',views.elimina,name='elimina'),  
    path('asigna',views.asigna,name='asigna'),  
    path('pendiente',views.pendiente,name='pendiente'),  
    path('clientesgeneral/', views.Clientes_General, name='clientesgeneral'),
    path('clientespendientes/', views.Clientes_pendientes, name='clientespendientes'),
    path('asignaciones/<int:IDD>', views.Clientes_Funcionario, name='asignaciones'),
    path('declaracionxcliente/<int:IDD>',views.Declaracion_Cliente, name='declaracionxcliente'),
    path('asigna_declaracion_clientes',views.Asigna_Declaracion_Clientes, name='asigna_declaracion_clientes'),
    path('asigna_declaracion/<int:cliente_id>/<int:colaborador_id>',views.Asigna_Declaracion, name='asigna_declaracion'),
    path('clientes_declaraciones/',views.VsListaclientes,name ='clientes_declaraciones'),  
    path('Carga_Clientes_Sin_Declaracion/',views.VsClientessindeclaraciones,name='Carga_Clientes_Sin_Declaracion'),
    path('VsListaclientesdatos/',views.VsListaclientesdatosa,name ='VsListaclientesdatos'),
    path('BuscarDeclaracionxCliente/<int:IDD>',views.VDeclaracion_Cliente_asignacion,name ='BuscarDeclaracionxCliente'),
    path('elimina_declaracion_cliente/<int:IDD>',views.velimina_declaracion_cliente,name='elimina_declaracion_cliente'),  
    path('busca_declaraciones_xclientessinasignar/<int:IDD>',views.vdeclaraciones_sin_asignar_al_cliente,name='busca_declaraciones_xclientessinasignar'),  
    path('agreganuevadeclaracion',views.vdeclaraciones_sin_asignar_al_cliente,name='agreganuevadeclaracion'),  
    path('vagregarunadeclaracion/',views.vagregarunadeclaracion,name='vagregarunadeclaracion'),   
    path('agregarclientefuncionario/',views.clienteafuncionario,name='agregarclientefuncionario'),  
    path('desasignaclienteafuncionario/<int:IDD>',views.vsdesasignaclienteafuncionario,name='desasignaclienteafuncionario'),  
    path('buscadeclaracion',views.vbuscadeclaracion,name='buscadeclaracion'),
    path('buscadeclaraciondatos/',views.vbuscadeclaraciondatos,name='buscadeclaraciondatos'),  
    path('buscadeclaraciondatosclientes/<int:IDD>',views.vbuscadeclaraciondatosclientes,name='buscadeclaraciondatosclientes'),         
    path('iniciadeclaracion/',views.viniciadeclaracion,name='iniciadeclaracion'),         
    path('dfuncionarios/',views.vsfuncionarios,name='dfuncionarios'),       
    path('funcionarioinicia/<int:idd2>/<int:idd>/',views.vsfuncionarioinicia,name='funcionarioinicia'),      
    path('declaracionxcliente_asignadas/<int:IDD>',views.vsDeclaraciones_Cliente, name='declaracionxcliente_asignadas'),      
    path('IniciaDeclaracion',views.vsDeclaraciones_Cliente, name='IniciaDeclaracion'),         
    path('ActivaDeclaracion_b/<int:idd>',views.vsActivaDeclaracion, name='ActivaDeclaracion_b'),
    path('CierraDeclaracion/<int:idd>',views.vsCierraDeclaracion, name='CierraDeclaracion'),
    path('SuspendeDeclaracion/<int:idd>',views.vsSuspendeDeclaracion, name='SuspendeDeclaracion'),
    path('StatusDeclaracion/',views.VstatusDeclaracion, name='StatusDeclaracion'),  
    path('VisionDeclaracion/',views.VsVisionDeclaracion, name='VisionDeclaracion'), 
    path('VerDeclaracion/',views.VsEstatusDeclaracion, name='VerDeclaracion'),
    path('ActivaSuspendida/<int:idd>',views.VsActivaSuspendida,name ='ActivaSuspendida'),    
    path('calendario/',views.VsCalendario,name ='calendario'),
    path('ConfirmaDeclaracion/',views.VsConfirmaDeclaracion,name ='ConfirmaDeclaracion'),
    path('VerDeclaracionHistoricas/',views.VsEstatusDeclaracionHistoricas, name='VerDeclaracionHistoricas'),    
    path('Confirma/<int:idd>',views.VsConfirma, name='Confirma'),    
    path('DeclaracionesConfirmadas/',views.VsDeclaracionesConfirmadasCerradas, name='DeclaracionesConfirmadas'),    
    path('VerDeclaracionHistoricasCerradas/',views.VsDeclaracionesConfirmadasCerradasAplicadas, name='VerDeclaracionHistoricasCerradas'),            
    path('Buscaporfecha/<str:fecha>',views.VsBuscaporfecha, name='Buscaporfecha'),
    path('AgregaDeclaracionCalendario/<str:fch>',views.VsAgregaDeclaracionCalendario, name='AgregaDeclaracionCalendario'),
    path('BorraCalendarioLinea/<int:linea>',views.VsCalendario_Tributario_lineaBorra, name='BorraCalendarioLinea'),
    path('calendariotributario',views.VsCalendarioTributario, name='calendariotributario'),
    path('Buscadeclaracionxan/<str:anSeleccionada>/',views.VsBuscadeclaracionxan, name='Buscadeclaracionxan'),   
    path('reasignacalendario/',views.VsReasignadeclaracion, name='reasignacalendario'),   
    path('Buscadeclaracionxm/<int:selectedYear>,<int:selectedMonth>/',Views_BuscaDeclaracionxm.VsBuscadeclaracionxm, name='Buscadeclaracionxm'),   
    path('ReasignaDeclaracionCalendario/<str:fecha_propuesta>',Views_BuscaDeclaracionxm.VsReasignaDeclaracionCalendario, name='ReasignaDeclaracionCalendario'),   
    path('pendiente_realizar/',Views_pendiente_realizar.VsPendiente_realizar, name='pendiente_realizar'),   
    path('Realizar_consulta/<str:selectedYear>,<str:selectedMonth>/',Views_pendiente_realizar.VsPendiente_realizar_consultas, name='Realizar_consulta'),
    path('historico_movimientos/',Views_Historico_Movimientos.VsHistorico_Movimientos, name='historico_movimientos'),
    path('Realizar_consulta_Historica/<str:selectedYear>,<str:selectedMonth>/',Views_Historico_Movimientos.VsMovimiento_Historico, name='Realizar_consulta_Historica'),
    
    # Menu de Funcionarios 
    path('Funcionarios/',Views_Funcionarios.VsCargaformula, name='Funcionarios'),
    path('VisorFuncionario/',Views_Funcionarios.VsVisor_Funcionarios, name='VisorFuncionario'),
    path('busqueda_historico_movimientos/',Views_Historico_Movimientos_Busqueda.VsHistorico_Movimientos, name='busqueda_historico_movimientos'),
    path('Historicomovimientosbuscar/',Views_Historico_Movimientos_Busqueda.VsMovimiento_Historicobusqueda, name='Historicomovimientosbuscar'),
    path('asignadasafuncionario/',Views_Funcionarios.Vsasignadasafuncionario, name='asignadasafuncionario'),
    path('ListaColaboradores/',Views_Funcionarios.VsListaColaboradores, name='ListaColaboradores'),  
    path('DetalleColaborador/<int:IDD>/', Views_Funcionarios.VsListaColaboradoresyclientes, name='DetalleColaborador'),
    
    # Menu de Clientes 
    path('clientes/',views.clientes, name= 'clientes'),
    path('clienteyfuncionario/', Views_Funcionarios.Vsclienteyfuncionario, name='clienteyfuncionario'),
    path('DetalleClienteColaborador/', Views_Funcionarios.VsDetalleClienteColaborador, name='DetalleClienteColaborador'),    
    path('clientesactivos/', Views_Beneficios.VsClientesActivos, name='clientesactivos'),
    path('VisorClientes/', Views_Beneficios.VsVisorClientes, name='VisorClientes'),
    path('VisorTipos/', Views_Beneficios.VsVisorTipos, name='VisorClientes'),       
        
        
    # Menu de Beneficios 
    path('Asigna_tipo',Views_Beneficios.Vsasigna_tipo,name='Asigna_tipo'),    
    path('Declara_Tipo/', Views_Beneficios.Vspyme, name='Declara_Tipo'),
    path('Tipoformulario/',Views_Beneficios.NuevoTipo,name='Tipoformulario'),  
    path('Stguarda_tipo',Views_Beneficios.Vsguarda_tipo,name='guarda_tipo'), 
    path('editar_tipo/<int:idTipo>',Views_Beneficios.editartipo,name='editar_tipo'),     
    path('elimina_tipo/<int:IDD>',Views_Beneficios.elimina,name='elimina'),  
    path('busca_beneficios/<int:IDD>',Views_Beneficios.Vsbusca_beneficios,name='busca_beneficios'), 
    path('elimina_tipo_g/<int:id>',Views_Beneficios.Vseliminabeneficio,name='elimina_tipo_g'), 
    path('obtener_datos_registro/<int:id>/',Views_Beneficios.Vsobtener_datos_registro,name='obtener_datos_registro'), 
    path('Visor_Beneficios/',Views_Beneficios.VsBeneficios_Visor,name='Visor_Beneficios'), 
    path('BNotificar/',Views_Beneficios.VsNotificaciones,name='BNotificar'), 
    path('BNotificar2/',Views_Beneficios.VsNotificaciones2,name='BNotificar2'),     
    path('Vslevanta_Stattus/',Views_Statttus.Vslevanta_Stattus,name='Vslevanta_Stattus'),    
    path('Buscaconcalendariofinal/<int:selectedYear>,<int:selectedMonth>/',Views_Statttus.VsDeclaracionesfinales,name='Buscaconcalendariofinal'),    

    # Reportes
    path('Rep_General_Declaracion/',Views_ReportesGenerales.Declaracion_General,name='Rep_General_Declaracion'),    
    path('Rep_Clientesasignar/',Views_ReportesGenerales.Reporte_Cliente_S_Asignar,name='Rep_Clientesasignar'),    

    # Seguridad
    path('GParametros/',Views_Utilitarios.VsParametros,name='GParametros'), 
    path('AjusteDeclaraciones/',Views_Utilitarios.VsAjuste_Declaracion,name='AjusteDeclaraciones'),  
    path('ConfirmaMes/<int:idd>',Views_Utilitarios.VsConfirmaMes, name='ConfirmaMes'),    
    path('bparametros/',Views_Utilitarios.VsParametrosDatos, name='bparametros'),    
    path('ConfirmaParametro/<int:IDreg>',Views_Utilitarios.VsParametrosConfirma, name='ConfirmaParametro'),    
    path('Rusuarios',Views_Utilitarios.VsRusuarios, name='Rusuarios'),    
    path('BuscaUsuarios/',Views_Utilitarios.VsBuscaUsuarios, name='BuscaUsuarios'),    
    path('CrearUsuario/',Views_Utilitarios.VsCreaUsuarios, name='CrearUsuario'),    
    path('Bitacora/',views.VsBitacora, name='Bitacora'),    
    
    
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#  path('Buscamovcalendario/<int:selectedYear>,<int:selectedMonth>/',Views_Statttus.VsDeclaracionesfinales,name='Buscamovcalendario'),        