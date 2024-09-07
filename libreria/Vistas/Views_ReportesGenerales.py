# Reporte General de Declaraciones 
import os 
import math 
from datetime import datetime
from io import BytesIO # IO
from reportlab.pdfgen import canvas
#from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.colors import HexColor, red
from reportlab.lib.styles import getSampleStyleSheet
from libreria.models import Historico_Declaraciones, declaracion,cliente_proveedor_cliente_proveedor,Asignacion
from django.http import HttpResponse
from django.db.models import Exists, Subquery,OuterRef ,Q
#from libreria.views import pendiente 


logo_path="declaracion/Parametros/logo.png"


# Reporte De Declaraciones General -- primer reporte se hace por separado 
def Declaracion_General(request): 
    archivo = "Declaraciones_Generales.pdf"   
    ubicacion = "declaracion/Reportes"
       
    file_path = os.path.join(ubicacion, archivo)   # busca y verifica si existe     
    if os.path.exists(file_path):                  # Verificar si el archivo ya existe y eliminarlo si es necesario
        os.remove(file_path)
        
    save_path = os.path.join(ubicacion, archivo)   # Define la ruta completa donde se guardará el archivo
          
    datos_decla = declaracion.objects.all().order_by('codigo')  # busca las declaraciones 
             
    buffer = BytesIO()     # Crear un buffer en memoria para el PDF
    
    c=canvas.Canvas(buffer,pagesize=letter)
    width, height = letter 
    
    styles = getSampleStyleSheet()
    style = styles['Normal']
    
    c.setLineWidth(.3) # ancho de linea 
    
    # fuente y tamaño 
    c.setFont('Helvetica',12)
    
    # crea encabezado 
    header_height = 3 * 20  # 72 puntos por pulgada
    new_image_height = header_height
    new_image_width = width           
        
    # Obtener la fecha y hora actual en el formato deseado
    datetime_now = datetime.now().strftime('%d/%m/%Y %I:%M:%S %p') 
    
    
    def agrega_encabezado():
        # fuente y tamaño 
        c.setFont('Helvetica',12)
         # color de letra     
        c.setFillColor("rgb(0, 32, 32)")                    
        # Dibujar el texto en el PDF
        c.drawString(233, height - 18,'SISTEMA DE DECLARACIONES')
        c.drawString(231, height - 33,'Reporte General de Declaraciones')
        c.drawString(257, height - 48, datetime_now)     
        # Encabezado      
        #c.rect(2, 140, 50, new_image_height+5, fill=0) 
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 17, height - 60, width=100, height=50)
        else:
           c.drawString(20, height - 60, "N/A")       
        
        # Distancia en los renclones                  
        c.setLineWidth(0.7)
        c.line(0, height - 74, 620, height - 74)    # Linea Superior
        
        # Datos Encabezado detalle especifico       
        c.drawString(16,  height - 72, "ID")
        c.drawString(65,  height - 72, "Código   -    Descripción")    
        c.drawString(445, height - 72, "Tiempo")
        c.drawString(510, height - 72, "Estado")
        #c.line(0, height - 110, 620, height - 110)      # Linea Central        
  
    def nueva_pagina():
        c.showPage()  # Finaliza la página actual
        c.setPageSize(letter)  # Reestablece el tamaño de la página
        agrega_encabezado()  # Agrega el encabezado en la nueva página        
  
    #  c.setStrokeColor('white')
    
    # pone encabezados
    agrega_encabezado()  
                                  
    # Datos del Detalle               
    y = height - 80 # posicion de los datos de inicio 
    numero_pagina  = 1
    total_paginas = 0
    #itera sobre el data pone el detalle     
    for i, lineas in enumerate(datos_decla):
            if y <75: # control del brinco y encabezado de pagina 
               nueva_pagina()
               y = height - 75  # reinicia 
               #     c.showPage() # finaliza la pagina e inicia otra 
               numero_pagina += 1
               
            c.drawRightString(40, y, str(lineas.IDDeclaracion))   # id
            cod = ' '+lineas.codigo
            det = '-'+lineas.detalle[:70]
            cdet = cod + det  # une el codigo y el detalle 
            deta = Paragraph(cdet,style)
            deta_with = 500 # establece el ancho del parrafo 
            deta_height = 40 # la altura del parrafo                 
            deta.wrap(deta_with,deta_height) # distribuye
            deta.drawOn(c, 65, y )
            
            estado_str = 'Activo' if lineas.estado else 'Inactivo'
            c.drawRightString(600, y, str(lineas.tiempo))
            c.drawRightString(650, y, estado_str)
           # c.drawRightString(485, y, lineas.observaciones)                         
            
            # Añadir el número de página y el total de páginas
            c.drawString(width - 100, 20, f'Página {numero_pagina} de {total_paginas}')
            y  -= 20
            
    total_paginas =  c.getPageNumber()  # Obtiene el total de páginas    
    buffer.seek(0)  # Regresa al inicio del buffer   

    # Segundo pase: Crear el PDF final con los números de página
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    agrega_encabezado()  

    # Reinicia el contador de página y `y`
    page_number = 1
    y = height - 95
    
    for i, lineas in enumerate(datos_decla):
        if y < 75:
            c.showPage()  # Finaliza la página actual
            c.setPageSize(letter)  # Reestablece el tamaño de la página
            agrega_encabezado()  # Agrega el encabezado en la nueva página
            y = height - 75  # Reinicia la posición `y`
            page_number += 1
        
        c.drawString(16, y, str(lineas.IDDeclaracion))   # ID
        cod = ' ' + lineas.codigo
        det = '-' + lineas.detalle[:63]
        cdet = cod + det  # Une el código y el detalle
        
        # Crear y dibujar el párrafo con estilo
        deta = Paragraph(cdet, style)
        deta_width = 460  # Ajusta el ancho del párrafo según sea necesario
        deta_height = 40
        deta.wrap(deta_width, deta_height)
        deta.drawOn(c, 65, y)
               
        estado_str = 'Activo' if lineas.estado else 'Inactivo'
        c.drawString(450, y, str(lineas.tiempo))
        c.drawString(500, y, estado_str)
        
        # Añadir el número de página y el total de páginas
        c.drawString(width - 100, 20, f'Página {page_number} de {total_paginas}')
        
        y -= 15  # Ajusta el espaciado entre renglones

    # debe de poner el fin de pagina             
    c.save()

    # Obtener el contenido del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Guardar el contenido del PDF en la ruta especificada
    with open(save_path, 'wb') as f:
        f.write(pdf)
        
    # Crear una respuesta HTTP con el contenido del PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    # lo guarda en disco 
    #response['Content-Disposition'] = 'attachment; filename="Declaraciones_Generales.pdf"'
    # lo muestra por pantalla 
    response['Content-Disposition'] = 'inline; filename=archivo'
    
    return response

# Encabezado General para los demás Reportes 
def encabezados_reportes(Titulo,Dato_Encabezado,ancho,alto,cia):   
        # Crear un buffer en memoria para el PDF
        buffer = BytesIO()    
        # define tamaño del reporte 
        c=canvas.Canvas(buffer,pagesize=letter)
        width, height = letter         
        styles = getSampleStyleSheet()
        style = styles['Normal']
    
        # ancho de linea 
        c.setLineWidth(.3)        
        # fuente y tamaño 
        c.setFont('Helvetica',12)        
         # color de letra     
        c.setFillColor("rgb(0, 32, 32)")                                    
        # crea encabezado 
        header_height = 3 * 20  # 72 puntos por pulgada
        new_image_height = header_height
        new_image_width = width            
        # fecha y hora actual  
        datetime_now = datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')                                                        
        # Dibujar el texto en el PDF
        c.drawString(227, height - 25.5, cia)
        c.drawString(225, height - 38,Titulo)
        c.drawString(245, height - 53, datetime_now)     
        # Encabezado - logo
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 17, height - 60, width=100, height=50)
        else:
           c.drawString(20, height - 60, "N/A")          
        #c.rect(2, 140, 50, new_image_height+5, fill=0)
        
        c.setLineWidth(0.5)
        c.line(0, height - 77, 620, height - 77)    # Linea Superior
        c.line(0, height - 64, 620, height - 64)      # Linea Central
        # Datos Encabezado detalle especifico       
        c.drawString(16,  height - 74, Dato_Encabezado)        
                
        #  c.line(0, height - 129.5, 620, height - 129.5)  # Linea Inferior 
        return buffer,c,width,height

def pie_reportes(c,Titulo,Dato_Encabezado):
        c.showPage()  # Finaliza la página actual
        c.setPageSize(letter)  # Reestablece el tamaño de la página
        encabezados_reportes(Titulo,Dato_Encabezado)  # Agrega el encabezado en la nueva página  

# Reporte Clientes sin Asignar 
def Reporte_Cliente_S_Asignar(request):    
    cia = "SISTEMA DE DECLARACIONES"
    archivo = "Clientes_sin_Asignar.pdf"   
    ubicacion = "declaracion/Reportes"
    file_path = os.path.join(ubicacion, archivo) # busca y verifica si existe 
        
    if os.path.exists(file_path):                # Verificar si el archivo ya existe y eliminarlo si es necesario
        os.remove(file_path)       
    save_path = os.path.join(ubicacion, archivo) # Define la ruta completa donde se guardará el archivo     
    styles = getSampleStyleSheet()
    style = styles['Normal']    
    # Busca datos de los clientes que no esta asignados a nadie 
    clientes_pendientes = cliente_proveedor_cliente_proveedor.objects.annotate(
        tiene_asignacion=Exists(
        Asignacion.objects.filter(
             IDClientes_Proveedores=OuterRef('IDClientes_Proveedores')
               )
            )
        ).filter(tiene_asignacion=False,Estado = True,Tipo = True) 
                
    cantidad_registros = clientes_pendientes.count()   # saca la cantidad de registros para el calculo de hojas
    total_Paginas = math.ceil(cantidad_registros / 50)  # Redondear hacia arriba y garantizar un entero

    Titulo = "Reporte de Clientes sin Asignacion"
    Encabezado=" ID          Nombre del Cliente                                      Correo                                                  Estado"
    
    buffer, c,width,height   = encabezados_reportes(Titulo, Encabezado,0,0,cia)
    numero_pagina = 1 
    y = height - 91
        
    for i, lineas in enumerate(clientes_pendientes):
        if y < 75:
            c.showPage()                                                               # Finaliza la página actual
            c.setPageSize(letter)                                                      # Reestablece el tamaño de la página
            buffer, c,width,height = encabezados_reportes(Titulo, Encabezado,0,0,cia)  # encabezado             
            y = height - 91                                                            # Reinicia la posición `y`
            numero_pagina  += 1                                                        # suma pagina 
        
        c.drawString(16, y, str(lineas.IDClientes_Proveedores))                  # ID        
        det   = lineas.Descripcion[:63]
        direc = lineas.Direccion[:50]
        cdet =  det+direc                                                        # Une el nombre y direccion 
        
        # Crear y dibujar el párrafo con estilo
        deta = Paragraph(cdet, style)
        c.drawString(236,y,lineas.Email)
        
        deta_width = 460  # Ajusta el ancho del párrafo según sea necesario
        deta_height = 40
        deta.wrap(deta_width, deta_height)
        deta.drawOn(c, 65, y)
               
        estado_str = 'Activo' if lineas.Estado else 'Inactivo'        
        c.drawString(500, y, estado_str)
        
        # Añadir el número de página y el total de páginas
        c.drawString(width - 100, 20, f'Página {numero_pagina} de {total_Paginas}')
        
        y -= 15  # Ajusta el espaciado entre renglones

    # debe de poner el fin de pagina             
    c.save()

    # Obtener el contenido del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Guardar el contenido del PDF en la ruta especificada
    with open(save_path, 'wb') as f:
        f.write(pdf)
        
    # Crear una respuesta HTTP con el contenido del PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    # lo guarda en disco 
    #response['Content-Disposition'] = 'attachment; filename="Declaraciones_Generales.pdf"'
    # lo muestra por pantalla 
    response['Content-Disposition'] = 'inline; filename=archivo'
    
    return response   


            
# Reporte Status de Declaraciones  
def Reporte_StatusDeclaracion(request):    
    cia = "SISTEMA DE DECLARACIONES"
    archivo = "StatusDeclaraciones.pdf"   
    ubicacion = "declaracion/Reportes"
    file_path = os.path.join(ubicacion, archivo) # busca y verifica si existe 
        
    if os.path.exists(file_path):                # Verificar si el archivo ya existe y eliminarlo si es necesario
        os.remove(file_path)       
    save_path = os.path.join(ubicacion, archivo) # Define la ruta completa donde se guardará el archivo     
    styles = getSampleStyleSheet()
    style = styles['Normal']    
    # Busca datos de los clientes que no esta asignados a nadie 
    
    Total_Declaraciones = Asignacion.objects.select_related(
        'IDClientes_Proveedores', 
        'IDPlanilla_Funcionarios', 
        'IDDeclaracion'
    ).all().order_by("Fecha_Presenta","Mes")
 
    datadeclaracion = list(Total_Declaraciones.values(
        'IDDeclaracion',  # Acceder al ID de la declaración relacionada
        'IDDeclaracion__codigo',
        'IDDeclaracion__detalle',
        'Fecha_Asigna',
        'Fecha_Presenta',
        'Rectificativa',
        'IDPlanilla_Funcionarios__Nombre',  # Acceder al nombre del funcionario
        'IDDeclaracion__tiempo',
        'IDDeclaracion__estado', 
        'IDDeclaracion__observaciones',
        'Iniciada',
        'Suspendida',        
        'IDClientes_Proveedores__IDClientes_Proveedores',
        'IDClientes_Proveedores__Descripcion',
        'IDClientes_Proveedores__Email',
        'Mes',
    ))       
                    
    cantidad_registros = len(datadeclaracion)   # saca la cantidad de registros para el calculo de hojas
    total_Paginas = math.ceil(cantidad_registros / 50)  # Redondear hacia arriba y garantizar un entero

    Titulo = "Estado General Declaraciones"
    Encabezado=" ID    Codigo       Asigno      Presenta     Mes       Funcionario  Estado  Inic Ssp Rect  Nombre"
    
    buffer, c,width,height   = encabezados_reportes(Titulo, Encabezado,0,0,cia)
    numero_pagina = 1 
    y = height - 91
        
    for i, lineas in enumerate(datadeclaracion):
        if y < 75:
            c.showPage()                                                               # Finaliza la página actual
            c.setPageSize(letter)                                                      # Reestablece el tamaño de la página
            buffer, c,width,height = encabezados_reportes(Titulo, Encabezado,0,0,cia)  # encabezado             
            y = height - 91                                                            # Reinicia la posición `y`
            numero_pagina  += 1                                                        # suma pagina 
        
        c.drawString(16, y, str(lineas['IDDeclaracion']))                  # ID        
        det   = lineas['IDDeclaracion__codigo'][:20]
        direc = lineas['IDDeclaracion__detalle'][:25]
        cdet =  det
        fchas = lineas['Fecha_Asigna'].strftime('%d/%m/%Y')  
        fchap = lineas['Fecha_Presenta'].strftime('%d/%m/%Y')         
        func  = lineas['IDPlanilla_Funcionarios__Nombre'][:10]
        ini   = lineas['Iniciada']
        estado_iniciada = 'No' if not ini else 'Sí'
        sus   = lineas['Suspendida']
        estado_susp = 'No' if not sus else 'Sí'
        rec   = lineas['Rectificativa'] 
        estado_rec = 'No' if not rec else 'Sí'
        cl         = lineas['IDClientes_Proveedores__Descripcion'][:25]
         
        # Crear y dibujar el párrafo con estilo
        deta = Paragraph(cdet, style)
        # c.drawString(236,y,lineas.Email)
        # Lista de nombres de meses (índices 1-12)
        nombres_meses = [
            '', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        
        
        # Convertir el número del mes a nombre del mes
        mes_numero = lineas['Mes']
        nombre_mes = nombres_meses[mes_numero] if 1 <= mes_numero <= 12 else 'Desconocido'
        
        
        deta_width = 460  # Ajusta el ancho del párrafo según sea necesario
        deta_height = 40
        deta.wrap(deta_width, deta_height)
        deta.drawOn(c, 65, y)
               
        estado_str = 'Activo' if lineas['IDDeclaracion__estado'] else 'Inactivo'       #
        
        c.drawString(95, y, fchas)              # fecha asignada
        c.drawString(160, y, fchap)             # fecha Presenta
        c.drawString(222, y, nombre_mes)        # mes
        c.drawString(275, y, func)              # nombre del funcionario 
        c.drawString(339, y, estado_str)        # estado
        c.drawString(390, y, estado_iniciada )  # si ya inicio o no 
        c.drawString(408, y, estado_susp )      # suspendida
        c.drawString(428, y, estado_rec )       # rectificativa
        c.drawString(450, y, cl )               # nombre del cliente 
        
        # Añadir el número de página y el total de páginas
        c.drawString(width - 100, 20, f'Página {numero_pagina} de {total_Paginas}')
        
        y -= 15  # Ajusta el espaciado entre renglones

    # debe de poner el fin de pagina             
    c.save()

    # Obtener el contenido del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Guardar el contenido del PDF en la ruta especificada
    with open(save_path, 'wb') as f:
        f.write(pdf)
        
    # Crear una respuesta HTTP con el contenido del PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    # lo guarda en disco 
    #response['Content-Disposition'] = 'attachment; filename="Declaraciones_Generales.pdf"'
    # lo muestra por pantalla 
    response['Content-Disposition'] = 'inline; filename=archivo'
    
    return response   

