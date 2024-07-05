from django.db import models
   
class declaracion(models.Model):
    IDDeclaracion=models.AutoField(primary_key=True)   
    codigo = models.CharField(max_length =10, verbose_name='Código', unique=True) 
    detalle = models.CharField(max_length =100 ,null =True) 
    tiempo = models.DecimalField(default = 30, max_digits = 5,decimal_places = 0,verbose_name='Tiempo') 
    estado = models.BooleanField(default = True)
    observaciones = models.TextField(blank=True, verbose_name='Observacion')
    imagen = models.ImageField(upload_to='imagenes/', null=True, verbose_name='Imagen')
    
    
    def __str__(self):
        fila = "Codigo: " + self.codigo + " - " + "Detalle: " + self.detalle 
        return fila 
    
    # borrar fisico de la imagen 
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()
        
class planillas_planilla_funcionarios(models.Model):
    IDPlanilla_Funcionarios = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=20)
    Estado = models.BooleanField(default=True) 
    
class cliente_proveedor_cliente_proveedor(models.Model):    
    IDClientes_Proveedores = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=180) 
    Direccion = models.TextField(null=True)
    Email =  models.CharField(max_length=250, null = True) 
    Fecha_Ult_Movimiento = models.DateTimeField(null=True)  
    Estado = models.BooleanField(default=True)
    
    def __str__(self):
        return "{}".format(self.Descripcion)
                      
class Asignacion(models.Model):
    IDAsignacion = models.AutoField(primary_key=True)
    Fecha_Presenta = models.DateField(blank=True,null=True, verbose_name='Fecha_Presenta')
    Fecha_Asigna = models.DateField(blank=True,null=True, verbose_name='Fecha_Asigna')
    Fecha_Proxima = models.DateField(blank=True,null=True, verbose_name='Fecha_Proxima')
    correo =models.BooleanField(default=False)
    Iniciada = models.BooleanField(default=False) 
    Suspendida = models.BooleanField(default=False)
    
    # llaves foraneas 
    IDClientes_Proveedores = models.ForeignKey(cliente_proveedor_cliente_proveedor, on_delete=models.CASCADE) 
    IDPlanilla_Funcionarios = models.ForeignKey(planillas_planilla_funcionarios, on_delete=models.CASCADE)
    IDDeclaracion = models.ForeignKey(declaracion, null=False, blank=False,  on_delete=models.CASCADE)           
    
    def __str__(self):
        return "{}".format(self.Fecha_Presenta)

# Define que declaraciones utiliza cada cliente 
class Declaracion_Clientes(models.Model):
    IDDeclaracion_Clientes = models.AutoField(primary_key=True)
    Fecha_Asigna = models.DateField(blank=True,null=True, verbose_name='Fecha_Asigna')
    Estado = models.BooleanField(default=False)
    Observacion = models.CharField(max_length=180)   
    # llaves foraneas 
    IDClientes_Proveedores = models.ForeignKey(cliente_proveedor_cliente_proveedor, on_delete=models.CASCADE)     
    IDDeclaracion = models.ForeignKey(declaracion, null=False, blank=False,  on_delete=models.CASCADE)           
    
    def __str__(self):
        return "{}".format(self.IDDeclaracion_Clientes)
    
# calendario Tributario 
class calendario_tributario(models.Model):
    IDCalendario_tributario=models.AutoField(primary_key=True)   
    Fecha_Presenta = models.DateField(blank=True,null=True, verbose_name='Fecha_Presenta')
    Observaciones = models.TextField(blank=True, verbose_name='Observacion')
     
     # llaves foraneas 
    IDDeclaracion = models.ForeignKey(declaracion, null=False, blank=False,  on_delete=models.CASCADE)           
                  
    def __str__(self):
        return f"Fecha Presentación: {self.Fecha_Presenta}, ID: {self.IDCalendario_tributario}"
        

class Historico_Declaraciones(models.Model):
    IDHistorico_Declaraciones = models.AutoField(primary_key=True)
    IDAsignacion = models.IntegerField(blank=True,null=False, verbose_name='IDAsignacion')
    Fecha_Presenta = models.DateField(blank=True,null=True, verbose_name='Fecha_Presenta')
    Fecha_Asigna = models.DateField(blank=True,null=True, verbose_name='Fecha_Asigna')
    Fecha_Proxima = models.DateField(blank=True,null=True, verbose_name='Fecha_Proxima')
    Fecha_Cierre  = models.DateField(blank=True,null=True, verbose_name='Fecha_Cierre' )
    correo =models.BooleanField(default=False)
    Iniciada = models.BooleanField(default=False) 
    Suspendida = models.BooleanField(default=False)
    Usuario_Cierre = models.CharField(max_length=100)  
    Numero_Comprobante = models.CharField(max_length=50)  
    Fecha_Final = models.DateTimeField(blank=True, null=True, verbose_name='Fecha_Final')        
    
    # llaves foraneas 
    IDClientes_Proveedores = models.ForeignKey(cliente_proveedor_cliente_proveedor, on_delete=models.CASCADE) 
    IDPlanilla_Funcionarios = models.ForeignKey(planillas_planilla_funcionarios, on_delete=models.CASCADE)
    IDDeclaracion = models.ForeignKey(declaracion, null=False, blank=False,  on_delete=models.CASCADE)              
    
    def __str__(self):
        return "{}".format(self.Fecha_Presenta)