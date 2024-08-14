# Reporte General de Declaraciones 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader 
# archivo a Generar 
archivo=canvas.Canvas("Declaraciones_Generales.pdf",pagesize=letter)


# ancho de linea 
archivo.setLineWidth(.3)

# fuente y tamaño 
archivo.setFont('Helvetica',14)

# detalle del texto x , y
archivo.drawString(120,760,'Detalle de Texto')

# posicion de linea 
archivo.line(120,700,590,747)

# circulos radui stroke  y relleno 
archivo.circle(120,720,20,1,1)

# imagenes 
logo = ImageReader('https://picsum.photos/200/200') 
canvas.drawImage(logo,10,240, widht = 50, height = 50, preserveAspectRatio = True)
archivo.save()

#mostrar_pdf('archvo.pdf')


# como convertir pdf en imagenes 
# pip install pdf2image 
from pdf2image import convert_from_path
pages = convert_from_path('archivo.pdf')
numero_pagina = 0
for page in pages:
    page.save(f'out_{numero_pagina}.jpg','JPEG')
    numero_pagina += 1
    


# configuracion basica para los reportes 
# Reporte General de Declaraciones 
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class Reporte:

    # inicia configuracion definiendo tipos de reporte 
    @staticmethod
    def inicial_reporte(modalidad, nombre_salida):
        
        try:                                         
            
            # Inicializar la respuesta PDF
            response = HttpResponse(content_type='application/pdf')
            
            # asigna el nombre del documento y el tipo si es para verlo o para descargarlo                            
            response['Content-Disposition'] = f'{modalidad}; filename="{nombre_salida}.pdf"'
            lienzo = letter #letter A4                                            
            c = canvas.Canvas(response, pagesize=lienzo) 
            width, height = lienzo
            return response, c, width, height, getSampleStyleSheet()    
            
        except Exception as e:
            raise Exception(f"{str(e)} - definicion_inicial_reporte()") 
        

        # ancho de linea 
        #c.setLineWidth(.3)
    # fuente y tamaño 
    #c.setFont('Helvetica',14)
    # crea encabezado 
    # Calcular la altura deseada del encabezado (por ejemplo, 2 pulgadas)
    #header_height = 2 * 50  # 72 puntos por pulgada

    # detalle del texto x , y
    #c.drawString(120,760,'Detalle de Texto')

    # posicion de linea 
    #c.line(120,700,590,747)

    # circulos radui stroke  y relleno 
    #c.circle(120,720,20,1,1)

    # imagenes 
    #logo = ImageReader('https://picsum.photos/200/200') 
    #canvas.drawImage(logo,10,240, widht = 50, height = 50, preserveAspectRatio = True)
    #archivo.save()

    #mostrar_pdf('archvo.pdf')


    # como convertir pdf en imagenes 
    # pip install pdf2image 
    #from pdf2image import convert_from_path
    #pages = convert_from_path('archivo.pdf')
    #numero_pagina = 0
    #for page in pages:
    #    page.save(f'out_{numero_pagina}.jpg','JPEG')
    #    numero_pagina += 1
    
