// Seguridad datos del parametro 
function StParametros(){        
      fetch(`/bparametros/`)
      .then(response => {                     
          if (!response.ok) {
              throw new Error('No se logró la consulta : ' + response.statusText);
          }
          
          // convierte la respuesta en json <td><a name="" id="" class="btn btn-secondary" href="#" onclick="Stfinaliza(${item.IDHistorico_Declaraciones})">Finalizar</a></td>
          return response.json();
            })
       .then(tparametroArray => {
                // Verifica si la respuesta es un array y toma el primer elemento
                if (Array.isArray(tparametroArray) && tparametroArray.length > 0) {
                    const tparametro = tparametroArray[0];  // No hay problema aquí, ya que es una nueva declaración
                    
                    document.getElementById('nombre').value = tparametro.Nombre !== null && tparametro.Nombre !== undefined ? tparametro.Nombre : '';
                    document.getElementById('basedatos').value = tparametro.Nombre_Base !== null && tparametro.Nombre_Base !== undefined ? tparametro.Nombre_Base : '';
                    document.getElementById('calendario').value = tparametro.Calendario !== null && tparametro.Calendario !== undefined ? tparametro.Calendario : '';
                    document.getElementById('puerto').value = tparametro.Puerto !== null && tparametro.Puerto !== undefined ? tparametro.Puerto : '';
                    document.getElementById('server').value = tparametro.Server !== null && tparametro.Server !== undefined ? tparametro.Server : '';
                    document.getElementById('usuario').value = tparametro.Usuario !== null && tparametro.Usuario !== undefined ? tparametro.Usuario : '';
                    document.getElementById('clave').value = tparametro.Clave !== null && tparametro.Clave !== undefined ? tparametro.Clave : '';
                    document.getElementById('idcia').value = tparametro.IDCia !== null && tparametro.IDCia !== undefined ? tparametro.IDCia : '';
                    document.getElementById('idreg').value = tparametro.IDParametros_Declaraciones !== null && tparametro.IDParametros_Declaraciones !== undefined ? tparametro.IDParametros_Declaraciones : '';

                    // Muestra la ubicación del archivo
                    const fileLocation = tparametro.Ubicacion_logo ? `Ubicación: ${tparametro.Ubicacion_logo}` : 'No disponible';
                    document.getElementById('file-info').textContent = fileLocation;                                       
                    
                } else {
                    console.warn('No se encontraron datos en la respuesta.');
                }                  
        })             
    .catch(error => {
     console.error('Fetch error:', error);
     });
    }




// Confirm los datos guardados en el parametro 
function StConfirmaparametros() {     
    // obtener los datos del formulario    
    var IDreg = document.getElementById('idreg').value ;  
    var idciaInput = document.getElementById('idcia').value;  // Obtener el valor como string
    var idcian = parseInt(idciaInput, 10);  // Convertir a entero    
    // variables de carga de datos cambiados
    var Cnombre = document.getElementById('nombre').value;
    var Cnombre_Base = document.getElementById('basedatos').value;
    var Cpuerto = document.getElementById('puerto').value;
    var Cserver = document.getElementById('server').value;
    var Cusuario = document.getElementById('usuario').value;
    var Cclave = document.getElementById('clave').value;
    var Cubicacion_Logo = document.getElementById('inputGroupFile04').value ;
    var Ccalendario = document.getElementById('calendario').value;

    Swal.fire({
        title: "Guardar datos del Parámetro",
        text: "¿Desea guardar los datos?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, proceder"
    }).then((result) => {
        if (result.isConfirmed) {            
            // Solicitud POST                                   
            fetch(`/ConfirmaParametro/${IDreg}`, {        
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()  // Asegúrate de que esta función esté definida
                },
                body: JSON.stringify({
                    nombre: Cnombre,
                    basedatos:Cnombre_Base,
                    puerto: Cpuerto,
                    server: Cserver,
                    usuario: Cusuario,
                    clave: Cclave,
                    idcia: idcian,
                    inputGroupFile04 :  Cubicacion_Logo,
                    calendario: Ccalendario,
                })             
            })                 
            .then(response => {                     
                if (!response.ok) {
                    throw new Error('Error: No se pudo confirmar la actualización');
                }                
                return response.json();
            })
            .then(data => {                
                if (data.success) {
                    // Indica que el dato llegó bien
                    Swal.fire({
                        title: "¡Actualizado!",
                        text: "Su registro fue actualizado.",
                        icon: "success"
                        
                    });
                    // Recarga la página
                    location.reload();  
                } else {
                    Swal.fire({
                        title: "Error",
                        text: "No se pudo actualizar el registro.",
                        icon: "error"
                    });
                }
            })
            .catch(error => {
                console.error('Error al confirmar la declaración:', error);
            });
        }
    });       
}


// Función para obtener el token CSRF
function getCSRFToken() {
    const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
    return csrfTokenElement ? csrfTokenElement.value : null;
}

// visor de usuarios 
function StUsuarios() {
    fetch(`/BuscaUsuarios/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('No se logró la consulta : ' + response.statusText);
            }
            return response.json();
        })
        .then(tusuarios => {
            const tbody = document.querySelector("#TablaUsuarios tbody");
            tbody.innerHTML = '';
            tusuarios.forEach(item => {
                const row = document.createElement("tr");
                row.innerHTML = `                        
                    <td>${item.id}</td>
                    <td>${item.username}</td>                
                    <td>${item.first_name}</td>                
                    <td>${item.last_name}</td>
                    <td>${item.email}</td>
                    <td>${item.is_active ? "Sí" : "No"}</td>
                    <td><a name="" id="" class="btn btn-primary" href="#"  role="button"><i class="bi bi-pencil"></i></a>
                        <a name="" id="" class="btn btn-danger"  href="#" onclick="eliminadecla({{a.IDDeclaracion}})"  role="button"><i class="bi bi-trash"></i></a>
                    </td>`;
                tbody.appendChild(row);
            });     
                 // Inicializa DataTables después de llenar la tabla
                 $('#TablaUsuarios').DataTable({
                    "language": {
                        "url": "{% static 'json/Spanish.json' %}"
                    },
                    "searching": true,
                    "ordering": true,
                    "responsive": true,
                    "columnDefs": [
                        { "width": "7%", "targets": [0] },
                        { "width": "7%", "targets": [1] },
                        { "width": "10%", "targets": [2] },
                        { "width": "10%", "targets": [3] },
                        { "width": "10%", "targets": [4] },
                        { "width": "10%", "targets": [5] },
                        { "width": "15%", "targets": [6] }
                    ]
                });            

        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
}


// Usuario Nuevo 
function StUsuarioNuevo() {

}