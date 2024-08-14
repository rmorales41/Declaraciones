
Stlistarfuncionario
document.addEventListener("DOMContentLoaded", function() {
    StListaclientes(); // Llama a la función para cargar el combo al cargar la página por primera vez  
});

let datosCargados = false;

// carga la lista de funcionarios // 
function listarfuncionarios() {
    // Obtener el valor seleccionado (nombre del funcionario) 
    var selectElement = document.getElementById("funcionarios");            
    // Obtener el ID del funcionario
    var selectedId = selectElement.options[selectElement.selectedIndex].value;
    llenarpendienteasigna();   
    Carga_ClienteFuncionario(selectedId);
  }

// busca los clientes pendientes de asignacion
async function llenarpendienteasigna() {    
    try {
       // limpia select 
       clientepend.innerHTML="";                 
       const response = await fetch("/clientespendientes/");  
       const data = await response.json();        
   
       if (data) {
           const select = document.getElementById("clientepend");
  
           data.data.forEach(item => {
               const option = document.createElement("option");
               option.value = item.IDClientes_Proveedores;
               // Crear un contenedor span para el texto y el botón
               const container = document.createElement("div");       
               // Establecer el texto del span
               container.textContent =  item.Descripcion;
               option.textContent = item.Descripcion;
               
                // Crear un botón
                const button = document.createElement("button");
                button.textContent = "Acción";
         
                // Agregar un evento de clic al botón
                button.addEventListener("click", () => {
                    // Realizar alguna acción cuando se hace clic en el botón
                    console.log("Botón clickeado para:", item.Descripcion);
                    // Por ejemplo, podrías llamar a una función con el ID del cliente
                    // realizarAlgunaAccion(item.IDClientes_Proveedores);
                });
         
         // Agregar el botón al contenedor
         container.appendChild(button);

               select.appendChild(option);
           });
       } else {
           console.error("Error al obtener los datos.");
       }
   } catch (error) {
       console.error("Error en la solicitud:", error);
   }
}

// Busca los clientes asignados al funcionario 
async function Carga_ClienteFuncionario(idd) {
    // Limpia el select
    Clientfunc.innerHTML = "";

    try {
        const response = await fetch(`/asignaciones/${idd}`);
        const data = await response.json();

        if (data && data.data && data.data.length > 0) {
            const select = document.getElementById("Clientfunc");
            const clientesUnicos = {};

            data.data.forEach(item => {
                // Almacena el cliente en el objeto clientesUnicos utilizando su ID como clave
                clientesUnicos[item.IDClientes_Proveedores_id] = item.Descripcion;
            });

            // Itera sobre los clientes únicos y agrega opciones al select
            Object.keys(clientesUnicos).forEach(clienteId => {
                const option = document.createElement("option");
                option.value = clienteId;
                option.textContent = clientesUnicos[clienteId];
                select.appendChild(option);
            });
        } else {
            console.error("Error al obtener los datos.");
        }
    } catch (error) {
        console.error("Error en la solicitud:", error);
    }
}


// se encarga de cargar las declaraciones que tiene cada cliente segun su funcionario
async function Carga_Declaracion_Cliente(idd) {    
       //  Clientfunc.innerHTML="";             
           
    try {        
           const response = await fetch(`/declaracionxcliente_asignadas/${idd}`);
           const data = await response.json();                                      
           if (data.length > 0) {
            const tbody = document.querySelector("tbody");
            tbody.innerHTML = ""; // Limpiar tbody antes de agregar nuevas filas
             
                data.forEach(declaracion => {       
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${declaracion.iddeclaracion}</td>
                    <td>${declaracion.codigo}</td>
                    <td>${declaracion.detalle}</td>
                    <td>${declaracion.presentada}</td>
                    <td>${declaracion.asignada}</td>  
                    <td scope="row" style="color: ${declaracion.correo ? 'black' : 'red'}">${declaracion.correo ? 'Enviado' : 'No Enviado'}</td>`;
                     tbody.appendChild(row);
                   });
           } else {
               console.error("Atención no se encontraron datos de declaraciones asignadas.");
           }           
    } catch (error) {
        console.error("Error en la solicitud:", error);
    }
} 

// actualiza el estado de la asignacion iniciada o detenida 
async function actualizarEstado(idDeclaracion, isChecked) {
    try {
        // Aquí deberías enviar una solicitud al servidor para actualizar el estado de la declaración
        // Por ejemplo, podrías hacer una solicitud POST a un endpoint específico
        // con el idDeclaracion y el nuevo estado (isChecked)
        console.log(`Declaración ${idDeclaracion} - Estado: ${isChecked ? 'Iniciada' : 'No Iniciada'}`);
    } catch (error) {
        console.error("Error al actualizar el estado:", error);
    }
}



// saca el index del cliente seleccionado en el select 
async function Clientessinasignacion() {
      var asignaDeclaracionURL = "/asigna_Declaracion/";            
      var select = document.getElementById("clientepend");       // obtiene el elemento del select 
      var selectedOption = select.options[select.selectedIndex]; // obtiene el indice de la opcion seleccionada            
      var selectedClientId = selectedOption.value;               // obtiene el valor                 
      
      var select = document.getElementById("funcionarios");          // obtiene el elemento de colaboradores  
      var selectedOption = select.options[select.selectedIndex]; // obtiene el indice de la opcion seleccionada
      var selectedColaboradorId = selectedOption.value;          // obtiene el valor del funcionario                       
      
   
    try {
        await fetch(asignaDeclaracionURL + selectedClientId + "/" + selectedColaboradorId);        
        location.reload();                              // Recarga la página si la asignación fue exitosa
    } catch (error) {
        console.error('Error al asignar declaración:', error);
    }    
  }

async function StListaclientes() {        
    try {
        let select = document.getElementById("ListaClientes");
  
        if (select) {           
            if (!datosCargados) {
                const response = await fetch(`/VsListaclientesdatos/`);
                const responseData = await response.json();   

                if (responseData.data.length > 0) {                  
                    responseData.data.forEach(item => {      
                        const option = document.createElement("option");
                        option.value = item.IDClientes_Proveedores;
                        option.textContent = item.Descripcion;
                        select.appendChild(option);                 
                    });                                                              
                    datosCargados = true;                                       
                }         
            }              
            // optiene el valor del id     
            var selectedOption = select.options[select.selectedIndex]; 
            var selectedClientId = selectedOption.value;                    

           await StDeclaracion_Cliente_asignacion(selectedClientId); 
           await Stdeclaracion_sin_asignar(selectedClientId);
           
        }
    } catch (error) {
        console.error("Error en StListaclientes:", error);
    }
}
// muestra la vista de los clientes que aun no tienen ninguna declaracion asignada 
async function StClientessinasignacion() {    
    const response = await fetch(`/Carga_Clientes_Sin_Declaracion/`);
    const responseData = await response.json();                      // Acceder al objeto que contiene el array
    const data = responseData.data;                                  // Acceder al array dentro de responseData
    var select = document.getElementById("clientepend");
    select.innerHTML = "";                                           // limpia en combo 
                                                                     // Verificar si data es un array
    if (Array.isArray(data)) {
        // Si es un array, iterar sobre cada elemento
        data.forEach(function(cliente) {
            var option = document.createElement("option");
            if (cliente.IDClientes_Proveedores) {        
                option.text = cliente.Descripcion; 
                option.value = cliente.IDClientes_Proveedores; 
            } else {
                console.error("Datos incompletos para el cliente:", cliente);
            }
            select.appendChild(option);                               // agrega los datos al combo 
        });
    } else {
        console.error("Los datos recibidos no se pueden leer:", data);
    }
}

// Declaraciones asignadas por cliente  todas las declaraciones que el cliente tiene para ser asignadas 
async function StDeclaracion_Cliente_asignacion(idd) {
    try {
        
        if (idd) {
            const response = await fetch(`/BuscarDeclaracionxCliente/${idd}`);
            const data = await response.json();     

            if (Array.isArray(data)) {
                const tbody = document.querySelector("tbody");
                tbody.innerHTML = ""; 

                data.forEach(declaracion => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${declaracion.iddeclaracion_clientes}</td>
                        <td>${declaracion.codigo}</td>
                        <td>${declaracion.detalle}</td>
                        <td>${declaracion.fecha}</td>                        
                        <td scope="row" style="color: ${declaracion.estado ? 'black' : 'red'}">${declaracion.estado ? 'Activa' : 'Inactiva'}</td>                                        
                        <td><a name="" id="" class="btn btn-danger" href="#" onclick="elimina_declaracion_cliente(${declaracion.iddeclaracion_clientes})" role="button">Borrar</a></td>                                                
                        `;
                    tbody.appendChild(row);
                });
            } else {
                console.error("Atención: No se encontraron datos de declaraciones asignadas o el formato de datos es incorrecto.");
            }  
        } else {
            console.error("El ID seleccionado es inválido.");
        }
    } catch (error) {
        console.error("Error en StDeclaracion_Cliente_asignacion:", error);
    }   
}

         
// muesta las declaraciones que aun no han sido asignadas 
async function Stdeclaracion_sin_asignar() {
    try {
            // Obtener el ID del cliente seleccionado
            var selectClientes = document.getElementById("ListaClientes");
            var idClienteSeleccionado = selectClientes.value;      
           
            // Realizar la solicitud al servidor para obtener las declaraciones sin asignar
            const response = await fetch(`/busca_declaraciones_xclientessinasignar/${idClienteSeleccionado}`);
            const responseData = await response.json();
    
            // Obtener el elemento del select de declaraciones
            let selectDeclaracion = document.getElementById("Declaracionsasignar");
            
            // Limpiar el select de declaraciones
            selectDeclaracion.innerHTML = '';            
            if (responseData.length > 0) {
                // Si hay datos, iterar sobre ellos y agregar opciones al select
                responseData.forEach(item => {                    
                    const option = document.createElement("option");
                    option.value = `${item.IDDeclaracion}`;
                    option.textContent = `${item.codigo} - ${item.detalle}`;
                    selectDeclaracion.appendChild(option);
                });
                console.log('Declaraciones sin asignar cargadas exitosamente');
            } else {
                console.log('No se encontraron declaraciones sin asignar para este cliente');
            }
        } catch (error) {
            console.error("Error al cargar las declaraciones sin asignar:", error);
        }
    }    

// permite agregar nuevas declaraciones al cliente 
function StAsigna_Nueva_Declaracion_Cliente() {
        try {
            // Obtener el token CSRF
            const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
            const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;
                  
            // Obtener el IDClientes_Proveedores del cliente seleccionado
            var clienteId = document.getElementById('ListaClientes');
            var seleccionclienteId = clienteId.value;
            // obtiene la declaracion seleccionada 
            var declaracion_numero = document.getElementById('Declaracionsasignar');
            var selecciondeclaracionID = declaracion_numero.options[declaracion_numero.selectedIndex].value;                    

            // trasforma la fecha 
            const currentDate = new Date();
            const formattedDate = ("0" + currentDate.getDate()).slice(-2) + "/" + ("0" + (currentDate.getMonth() + 1)).slice(-2) + "/" + currentDate.getFullYear();
    
            const data = {
                Fecha_Asigna: formattedDate,
                Estado: true,
                Observacion: 'Registro Nuevo',
                clienteID: seleccionclienteId,
                declaracionID: selecciondeclaracionID,
            };                    
    
            fetch('/vagregarunadeclaracion/', {            
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data),
            })
            .then(response => {
                if (response.ok) {
                    console.log('Nueva declaración cliente agregada correctamente.');                  
                    // recarga datos 
                    StListaclientes();
                } else {
                    console.error('Error al agregar nueva declaración cliente:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Error en la función StAsigna_Nueva_Declaracion_Cliente:', error);
            });
        } catch (error) {
           console.error('Error en la función StAsigna_Nueva_Declaracion_Cliente:', error);
        }
    }
    
   
// Permite agregar clientes a funcionarios 
function Stagregacliente_a_funcionario() {
    // Obtener el token CSRF
    const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
    const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;

    // Obtener el IDClientes_Proveedores del cliente seleccionado pendiente de asignar 
    var clienteId = document.getElementById('clientepend');
    var selectedOptionCliente = clienteId.options[clienteId.selectedIndex].value; 
    
    // Obtener el ID Del funcionario 
    var funcionarioId = document.getElementById('funcionarios');
    var selectedOptionFuncionario = funcionarioId.options[funcionarioId.selectedIndex].value; 

    // Transformar la fecha 
    const currentDate = new Date();
    const formattedDate = ("0" + currentDate.getDate()).slice(-2) + "/" + ("0" + (currentDate.getMonth() + 1)).slice(-2) + "/" + currentDate.getFullYear();        

    const data = {
        Fecha_Presenta: formattedDate,
        Fecha_Asigna: formattedDate,
        Fecha_Proxima: formattedDate,
        correo: false,
        IDClientes_Proveedores: selectedOptionCliente,
        IDPlanilla_Funcionarios: selectedOptionFuncionario,
    };       
    fetch('agregarclientefuncionario/', {            
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data),
    })    
    .then(response => {        
        if (response.ok) {
            console.log('Nueva declaración cliente agregada correctamente.');                  
            // Recarga datos    
            location.reload();     
            StListaclientes();
        } else {
            console.error('Error al agregar nueva declaración cliente:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error en la función Stagregacliente_a_funcionario:', error);
    });
} 


// confirmacion de que quiere eliminar al cliente del funcionario 
function confirmarEliminacion() {
    return Swal.fire({
        title: "Desea Desligar al Cliente del Funcionario.? ",
        text: "El cliente queda disponible para ser asignado a otro funcionario",
        icon: "warning",
        showCancelButton: true,
        cancelButtonText: "No, Cancelar",
        confirmButtonText: "Si, Desligar",
        reverseButtons: true,
        confirmButtonColor: "#dc3545",
        backdrop: true,
        showLoaderOnConfirm: true,
    });
}


// Quita el cliente asignado al funcionario  Desasigna 
function Stdesasignacliente_a_funcionario() {
    confirmarEliminacion().then((result) => {
        if (result.isConfirmed) {
            // El usuario ha confirmado, procede con la eliminación
            const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
            const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;

            var clientefId = document.getElementById('Clientfunc');
            var selectedOptionCliente = clientefId.options[clientefId.selectedIndex].value;

            fetch(`/desasignaclienteafuncionario/${selectedOptionCliente}`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error en la respuesta de la red: ' + response.statusText);
                    }
                    return response.json();
                })
                .then(data => {
                    $(`#fila-${selectedOptionCliente}`).remove(); // Suponiendo que IDRegistro está definido en otro lugar
                    // Recargar la página
                     location.reload();
                 
                    
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}

// Muestra todas las declaraciones del sistema 
function StLista_Declaraciones() {               
        // Obtén el elemento <select> por su ID
        let select = document.getElementById("ldeclaraciones");
        // Limpia cualquier opción existente
        select.innerHTML = '';
        // Hace la consulta al url para ejecutar la vista buscadeclaraciondatosclientes
        //buscadeclaraciondatos
        fetch('buscadeclaraciondatos/')
        .then(response => {                     
            if (!response.ok) {
                throw new Error('Error en la respuesta de la red: ' + response.statusText);
            }
            // convierte la respuesta en json 
            return response.json();
        })
        .then(data => {                          
            // Verifica si 'ldeclaraciones' existe en los datos devueltos y lo verifica
            if (data.hasOwnProperty('ldeclaraciones') && Array.isArray(data.ldeclaraciones)) {
                const ldeclaraciones = data.ldeclaraciones;                
                if (data.ldeclaraciones.length > 0) {
                    select.innerHTML = ''; 
                        ldeclaraciones.forEach(item => {
                        const option = document.createElement("option");
                        option.value = item.IDDeclaracion;
                        option.textContent = `${item.codigo} - ${item.detalle}`;
                        select.appendChild(option);
                    });
                }
            } else {
                console.error("No se encontró el array 'ldeclaraciones' en los datos devueltos.");
            }
        })
        .catch(error => {
            console.error("Error en StLista_Declaraciones:", error);
        });
    } 

// muestra los clientes asociados a esa declaracion 
function StLista_Declaraciones_datos() {  
    let declaracionId = document.getElementById('ldeclaraciones');
    let IDD = declaracionId.options[declaracionId.selectedIndex].value;

    
    fetch(`buscadeclaraciondatosclientes/${IDD}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta de la red: ' + response.statusText);
            }
            return response.json(); // Devuelve el JSON para que el siguiente then lo tome        
        }).then(data => {
            const tbody = document.querySelector("tbody"); // Selecciona el tbody
            tbody.innerHTML = ''; // Limpia el tbody antes de insertar nuevas filas

            if (data.hasOwnProperty('data') && Array.isArray(data.data)) {
                data.data.forEach(cliente_proveedor => {                    
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${cliente_proveedor.IDClientes_Proveedores}</td>
                        <td>${cliente_proveedor.IDClientes_Proveedores__Descripcion}</td>
                        <td>${formatDate(cliente_proveedor.IDClientes_Proveedores__Fecha_Ult_Movimiento)}</td>`;
                    const cell = document.createElement("tr");

                        if (cliente_proveedor.IDClientes_Proveedores__Estado) {
                            cell.textContent ="Activo";
                            cell.style.color ="red";                            
                        } else {
                            cell.textContent ="Inactivo";
                            cell.style.color = "black";
                        }
                    row.appendChild(cell);
                    tbody.appendChild(row);
                });
            } else {
                console.error('La estructura de datos no es la esperada:', data);
            }
        })
        .catch(error => {
            console.error('Error al obtener los datos:', error);
        });
}

// Función para formatear la fecha en dd/mm/yyyy

function formatDate(dateString) {             
   // moment().format();         
    // Extrae el día, mes y año
    //console.log(dateString)
    const date = moment(dateString);     
    const day = date.date();
    const month = date.month() + 1; // getMonth devuelve 0 para enero, por eso se suma 1
    const year  = date.year();
   // const day   = fecha.date();

   // fecha = datetime.strptime(fecha, '%d-%m-%y').date()
   // const fecha_dia = day < 10 ? '0' + day : day;
   // const fecha_mes = month < 10 ? '0' + month : month;

    // Asegura dos digitos 
    const formattedDay = day < 10 ? '0' + day : day;
    const formattedMonth = month < 10 ? '0' + month : month;

    // Retorna la fecha formateada en formato dd/mm/yyyy
    return `${formattedDay}-${formattedMonth}-${year}`;
    //return `${fecha_dia}-${fecha_mes}-${year}`;
}


// Carga la lista de los funcionarios para asignacion de trabajos 
function Stlistarfuncionario(){
        // Obtener el valor seleccionado (nombre del funcionario) 
        var selectElement = document.getElementById("funcionarios");
        // Limpiar select     
        selectElement.innerHTML = "";   
        
        try {
            fetch(`/dfuncionarios/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error en la respuesta de la red: ' + response.statusText);
                    }
                    return response.json(); // Devuelve el JSON para que el siguiente then lo tome    
                })
                .then(data => {                          
                    // Verificar si 'datafuncionario' contiene los datos esperados
                    if (Array.isArray(data.datafuncionario) && data.datafuncionario.length > 0) {
                        const lfuncionarios = data.datafuncionario;
                        
                        lfuncionarios.forEach(item => {
                            const option = document.createElement("option");
                            option.value = item.IDPlanilla_Funcionarios;
                            option.textContent = `${item.IDPlanilla_Funcionarios} - ${item.Nombre}`;
                            selectElement.appendChild(option);
                        });
                    } else {
                        console.error("No se encontró el array 'datafuncionario' en los datos devueltos o está vacío.");
                    }
                })
                .catch(error => {
                    console.error('Error al obtener datos:', error);
                });
        } catch (error) {
            console.error('Error en la solicitud fetch:', error);
        }
    }

    // busca los clientes del funcionario 
    function BuscaClienteFuncionario() {
        let funcionarioId = document.getElementById('funcionarios');
        let idd = funcionarioId.options[funcionarioId.selectedIndex].value;        
        Carga_ClienteFuncionario(idd)    
    } 
    
 // busca las declaraciones del cliente asignado para iniciarlas 
    function StDeclaracion_Cliente_Inicia() {  
        let proveeId = document.getElementById('Clientfunc');     
        let idd2 = proveeId.options[proveeId.selectedIndex].value;                    
        let funcionarioId = document.getElementById('funcionarios');
        let idd = funcionarioId.options[funcionarioId.selectedIndex].value;           
        fetch(`/funcionarioinicia/${idd2}/${idd}/`)   
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta de la red: ' + response.statusText);
                }
                return response.json();        
            })
            .then(datadeclaracion => {                
                const tbody = document.querySelector("tbody"); 
                tbody.innerHTML = '';                                 
                    
                datadeclaracion.forEach(item => {                    
                    const row = document.createElement("tr");
                    const fechaProxima = new Date(item.Fecha_Proxima);
                    const fechaActual = new Date();
                    const diffTiempo = fechaProxima.getTime() - fechaActual.getTime();
                    const diffDias = Math.ceil(diffTiempo / (1000 * 60 * 60 * 24));
                    
                    let diasRestantesHTML = '';                    
                    let botoneshtml ='' ;                
                    diasRestantesHTML = `<td>${diffDias} días</td>`; // calcula dias                                                                             
                    if (item.IDDeclaracion__estado){
                        let Tipo ="";
                        if (item.Suspendida){                            
                            Tipo="Reinicia"
                        }else{
                            Tipo="Cerrar"
                        }
                        if (item.Iniciada){
                            botoneshtml =`
                            <td>
                                <a name="" id="" class="btn btn-info" >Labor</a>
                                <a name="" id="" class="btn btn-danger"  href="#" onclick="StDetenerDeclaracion(${item.IDAsignacion},'${Tipo}')" role="button">${Tipo}</a>
                            </td>  `;    
                        }else {                           
                            botoneshtml =`                         
                            <td>
                                <a name="" id="" class="btn btn-primary" href="#" onclick="StIniciaDeclaracion(${item.IDAsignacion},${item.Mes})" role="button">Iniciar</a>                                
                                <a name="" id="" class="btn btn-danger"  href="#"  role="button">Cierra</a>
                            </td>  `;
                        }
                    }else {
                        if(!item.IDDeclaracion__estado){    
                                                                  
                        diasRestantesHTML = `<td>Inactiva</td>`;
                        }                                                
                    }                                                      
                    row.innerHTML = `
                        <td>${item.IDAsignacion}</td>
                        <td>${item.IDDeclaracion__codigo}</td>
                        <td>${item.IDDeclaracion__detalle}</td>
                        <td>${formatDate(item.Fecha_Presenta)}</td>
                        <td>${formatDate(item.Fecha_Asigna)}</td>
                        <td>${item.IDDeclaracion__tiempo}</td>
                        <td>${formatDate(item.Fecha_Proxima)}</td>
                        ${diasRestantesHTML}
                        <td>${item.IDDeclaracion__estado ? "Activo" : "Inactivo"}</td>
                        <td>${item.correo ? "Sí" : "No"}</td>  
                        <td>${item.Iniciada && item.Suspendida ? "Suspendida" : item.Iniciada ? "Iniciada" : item.Suspendida ? "Suspendida" : "Sin actividad"}</td>                                                                      
                        <td><input type="checkbox" id ="checkbox-${item.IDAsignacion}" ${item.Rectificativa ? 'checked' : ''} /></td>                        
                        ${botoneshtml}`;   // pone los botones si esta activo || esto es or && esto es and 
                    tbody.appendChild(row);

                });
                   // Verifica el estado de los checkboxes
                    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                    console.log(`Checkbox ID: ${checkbox.id}, Checked: ${checkbox.checked}`);
            });
            })
            .catch(error => {
                console.error('Error al obtener los datos:', error);
            });
    }
    
    // esta funcion pertenece al modelo de Asignacion para el inicio de las declaraciones
  
// Esta función pertenece al modelo de Asignacion para el inicio de las declaraciones
function StIniciaDeclaracion(asignacionId,mes) { 
    // Variables de cambio del formulario 
    const controlck = document.getElementById('checkbox-' + asignacionId.toString());  
    const isCheck = controlck.checked; // a ver si esta marcado     
    // verifica estado 
    const isChecked = isCheck;


    return Swal.fire({
        text: `En el momento de dar por iniciada el sistema modificar la fecha de asignación con la fecha actual y ajustara la fecha Maxima de Presentación sumandole el indicador de días por declaración, la declaracion a iniciar es la del mes ${mes}.`,
        icon: "warning",
        showCancelButton: true,
        cancelButtonText: "No, Retroceder",
        confirmButtonText: "Si, Iniciar",
        reverseButtons: true,
        confirmButtonColor: "#dc3545",
        backdrop: true,
        showLoaderOnConfirm: true,
    }).then((result) => {            
        if (result.isConfirmed) {                                
            const csrfToken = getCSRFToken(); // Llama a la función correctamente
            console.log('Sending CSRF Token:', csrfToken); // Verifica el token enviado

            return fetch(`/ActivaDeclaracion_b/${asignacionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Usa el valor del token aquí
                },
                body: JSON.stringify({
                    rectificativa: isChecked ? 'on' : 'off',                    
                })
            }).then(response => {
                if (!response.ok) {
                    throw new Error(`Error ${response.status}: ${response.statusText}`);
                }
                return response.json();
            }).then(data => {                
                return Swal.fire("¡Registro actualizado!", data.message, "success");              
            }).then(() => {
                location.reload();
            }).catch(error => {
                Swal.fire("Error", error.message, "error");
            });                                
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            console.log("El usuario canceló la acción.");
        }            
    });        
}

// Función para obtener el token CSRF desde una metaetiqueta en el HTML    
//function getCSRFToken() {
//    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
//}
 

// suspende o cierra finaliza o suspende la declaracion iniciada -aqui
    function StDetenerDeclaracion(asignacionId,botontexto) {         
              
        return Swal.fire({                            
            text: "Con esta función podrá suspender la ejecución pero las fechas no se cambiarán, el tiempo sigue corriendo. Si cierra la declaración se actualizará la fecha de Presentada con la fecha máxima preparando para la próxima presentación...",
            icon: "warning",
            showDenyButton: true,
            showCancelButton: true,
            cancelButtonText: "Retroceder",
            confirmButtonText: "Cerrar Declaración",
            reverseButtons: true,
            denyButtonText: botontexto == 'Cerrar' ? 'Suspender' : 'Reinicia'  
        }).then((result) => {            
            if (result.isConfirmed) {                  
                fetch(`/CierraDeclaracion/${asignacionId}`)                               
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error al actualizar el registro');       
                    }
                    return response.json();
                })
                .then(data => {
                         // Mostrar mensaje de éxito
                         Swal.fire("¡Registro actualizado!", data.message, "success")               
                .then(() => {
                        // Actualizar los registros cambiados
                        location.reload();                       
                            });                   
                             })
                .catch(error => {                    
                    // Mostrar mensaje de error
                    Swal.fire("Informa", 'No hay registros por actualizar', "error");
                });                                                                            
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                // Boton  Retroceder devuelve el control sin hacer nada  
                console.log("El usuario canceló la acción.");                
            } else if (result.desmiss === Swal.DismissReason.deny) {            
                if (botontexto ==='Reinicia'){
                 // aqui debe de poner la declaracion iniciada y quitar la suspencion 
                 fetch(`/ActivaSuspendida/${asignacionId}`)
                 .then(response => {                    
                    if (!response.ok){
                        throw new Error('Error al actualizar el registro suspendido');       
                    }
                    Swal.fire("¡Registro Activado actualizado!", "Se activa de nuevo la declaracion")                     
                    .then(() => {
                        // Actualizar los registros cambiados
                        location.reload();                       
                    });

                 })
                } else {
                 // boton de suspender , llama a la vista para salvar el indicador 
                 fetch(`/SuspendeDeclaracion/${asignacionId}`)
                 .then(response => {
                    console.log(response)
                    if (!response.ok) {                        
                        throw new Error('Error al actualizar el registro');       
                    }
                    Swal.fire("¡Registro Suspendido actualizado!", "Se encuentra suspendido actualmente")                         
                    location.reload();  
                     })
                }
            }
        });          
    }
   
// busca el estado de las declaraciones 
function StStatusDeclaraciones() {      
    fetch(`/VerDeclaracion/`) 
    .then(response => {       
        if (!response.ok) {
            throw new Error('Error: No se pueden mostrar los datos');
        }       
       return response.json();        
    })
    .then(datadeclaracion => {
        const tbody = document.querySelector("tbody"); 
        tbody.innerHTML = '';                                 
            
        datadeclaracion.forEach(item => {                    
            const row = document.createElement("tr");
            const fechaProxima = new Date(item.Fecha_Presenta);
            const fechaAsignada = new Date(item.Fecha_Asigna);
            const fechaActual = new Date(); // fecha actual
            const diffTiempo = fechaProxima.getTime() - fechaActual.getTime();
            const diffDias = Math.ceil(diffTiempo / (1000 * 60 * 60 * 24));
            
            let diasRestantesHTML = `<td>${diffDias} días</td>`; // Calcula días restantes
                                                                             
          row.innerHTML = `
                <td>${item.IDDeclaracion}</td>
                <td>${item.IDDeclaracion__codigo}</td>
                <td>${item.IDDeclaracion__detalle}</td>
                <td>${formatDate(item.Fecha_Asigna)}</td>
                <td>${formatDate(item.Fecha_Presenta)}</td>
                ${diasRestantesHTML}                
                <td>${item.IDPlanilla_Funcionarios__Nombre}</td>              
                <td>${item.IDDeclaracion__estado ? "Activo" : "Inactivo"}</td>                
                <td>${item.Iniciada == 1 && item.Suspendida == 0 ? "Iniciada" : (item.Iniciada == 1 && item.Suspendida == 1 ? "Suspendida" : "Cerrada")}</td> `

            tbody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error al obtener los datos:', error);
    });
}

// Muestra todas las declaraciones del sistema 
function StCalendario_Tributario_old() { 
                  
   //  Limpia cualquier opción existente
   // select.innerHTML = '';
    // Obtén el elemento <select> por su ID
    let select = document.getElementById("lcalendario");
    select.innerHTML = '';
  // Hace la consulta al url para ejecutar la vista 
    fetch(`/buscadeclaraciondatos/`)     
    .then(response => {        
       if (!response.ok) {
           throw new Error('Error en la respuesta de la red: ' + response.statusText);
       }       
        // convierte la respuesta en json         
        return response.json();
     
        
    })
    .then(data => {              
    // Verifica si 'ldeclaraciones' existe en los datos devueltos y lo verifica
       if (data.hasOwnProperty('ldeclaraciones') && Array.isArray(data.ldeclaraciones)) {
            const ldeclaraciones = data.ldeclaraciones;

        if (data.ldeclaraciones.length > 0) {
                ldeclaraciones.forEach(item => {
                const option = document.createElement("option");
                option.value = item.IDDeclaracion;
                option.textContent = `${item.codigo} - ${item.detalle}`;
                select.appendChild(option);
              });
           }
         
       } else {
           console.error("No se encontró el array 'ldeclaraciones' en los datos devueltos.");
        } 
    }) 
  //  .catch(error => {
   //     console.error("Error en StLista_Declaraciones:", error);
   // });
} 


// aqui estoy 
function StCalendario_Tributario() {
    // Obtén el elemento <select> por su ID
    let select = document.getElementById("lcalendario");
    let tbody = document.getElementById("tbody_id");
    select.innerHTML = '';           
    // Hace la consulta al URL para ejecutar la vista     
    fetch(`/buscadeclaraciondatos/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta de la red: ' + response.statusText);
            }
            // Convierte la respuesta en JSON            
            return response.json();
        })
        .then(data => {
            // Verifica si 'ldeclaraciones' existe en los datos devueltos y lo verifica
            if (data.hasOwnProperty('ldeclaraciones') && Array.isArray(data.ldeclaraciones)) {
                const ldeclaraciones = data.ldeclaraciones;

                if (ldeclaraciones.length > 0) {
                    ldeclaraciones.forEach(item => {
                        const option = document.createElement("option");
                        option.value = item.IDDeclaracion;
                        option.textContent = `${item.codigo} - ${item.detalle}`;
                        select.appendChild(option);
                    });                    
                } else {
                    console.error("El array 'ldeclaraciones' está vacío.");
                }
            } else {
                console.error("No se encontró el array 'ldeclaraciones' en los datos devueltos.");
            }
        })
        .catch(error => {
            console.error("Error en StCalendario_Tributario:", error);
        });
}


// confirmacion de declaraciones 
function StStatushistoricoDeclaraciones() {
    fetch(`/VerDeclaracionHistoricas/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error: No se pueden mostrar los datos');
            }
            return response.json();
        })
        .then(datadeclaracion => {
            const tbody = document.querySelector("tbody");
            tbody.innerHTML = '';

            datadeclaracion.forEach(item => {
                const row = document.createElement("tr");
                const fechaProxima = new Date(item.Fecha_Presenta);
                const fechaAsignada = new Date(item.Fecha_Asigna);
                const fechaActual = new Date(); // fecha actual
                const diffTiempo = fechaProxima.getTime() - fechaActual.getTime();
                const diffDias = Math.ceil(diffTiempo / (1000 * 60 * 60 * 24));

                let diasRestantesHTML = `<td>${diffDias} días</td>`; // Calcula días restantes                                                                          
                row.innerHTML = `
                    <td>${item.IDHistorico_Declaraciones}</td>
                    <td>${item.IDDeclaracion__codigo}</td>                
                    <td>${item.IDClientes_Proveedores__IDClientes_Proveedores}</td>
                    <td>${item.IDClientes_Proveedores__Descripcion}</td>
                    <td>${formatDate(item.Fecha_Asigna)}</td>
                    <td>${formatDate(item.Fecha_Presenta)}</td>
                    <td>${formatDate(item.Fecha_Cierre)}</td>                          
                    <td>${item.IDPlanilla_Funcionarios__Nombre}</td>              
                    <td>${item.rectificativa ? "Si" : "No"}</td>  
                    <td>
                        <select id="correo_${item.IDHistorico_Declaraciones}" name='correo'>
                            <option value ='Si' selected>Si</option>
                            <option value ='No'>No</option>
                        </select>
                    </td>      
                    <td><input type="text" id="numero_comprabante_${item.IDHistorico_Declaraciones}" name="numero_comprobante" value="" placeholder='Comprobante'></td>                
                    <td><input type="date" id="fecha_cierre_${item.IDHistorico_Declaraciones}" name="fecha_cierre"></td>                      
                    <td><a name="" id="" class="btn btn-warning" href="#" onclick="StConfirma(${item.IDHistorico_Declaraciones})">Confirma</a></td>`;
              
                tbody.appendChild(row);
                //<td>${item.IDDeclaracion__estado ? "A" : "I"}</td>  
                // Agregar un listener para detectar cuando se selecciona la fecha en el input
                const inputFecha = document.getElementById(`fecha_cierre_${item.IDHistorico_Declaraciones}`);
                inputFecha.addEventListener("focus", function() {
                // Obtener la fecha actual
                const fechaActual = new Date();
                // Formatear la fecha actual para que sea compatible con el formato del input de fecha
                const formattedFechaActual = fechaActual.toISOString().split("T")[0];
                // Establecer el valor del input de fecha como la fecha actual
                inputFecha.value = formattedFechaActual;
                });
            });       
        })
        .catch(error => {
            console.error('Error al obtener los datos:', error);
        });
}


// ajuste de confirma con calendarios 
function StConfirma(idHistoricoDeclaraciones) { 
    // obtener los datos del formulario    
    var Numero_C = document.getElementById('numero_comprabante_'+idHistoricoDeclaraciones.toString()).value;
    var Fecha_C = document.getElementById('fecha_cierre_'+idHistoricoDeclaraciones.toString()).value;
    var Correo_C = document.getElementById('correo_'+idHistoricoDeclaraciones.toString()).value;
   
    Swal.fire({
        title: "Confirmador de Declaraciones",
        text: "¿Desea continuar con la confirmación de esta línea?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, proceder"
    }).then((result) => {
        if (result.isConfirmed) {            
            // Solicitud POST                                   
            fetch(`/Confirma/${idHistoricoDeclaraciones}`, {        
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken() 
                },
                body: JSON.stringify({
                    numero_comprobante: Numero_C,
                    fecha_cierre: Fecha_C,
                    correo: Correo_C,                 
                })        
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error: No se pudo confirmar la declaración');
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







// valida los datos para cerrar la confirmacion de declaraciones realizadas
function StConfirma_old(idHistoricoDeclaraciones) {    
    var Numero_C = document.getElementById('numero_comprabante_'+idHistoricoDeclaraciones.toString()).value;
    var Fecha_C = document.getElementById('fecha_cierre_'+idHistoricoDeclaraciones.toString()).value;
    var Correo_C = document.getElementById('correo_'+idHistoricoDeclaraciones.toString()).value;
   
    Swal.fire({
        title: "Confirmador de Declaraciones",
        text: "¿Desea continuar con la confirmación de esta línea?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, proceder"
    }).then((result) => {
        if (result.isConfirmed) {            
            // Solicitud POST                                   
            fetch(`/Confirma/${idHistoricoDeclaraciones}`, {        
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken() 
                },
                // empaca datos para el server 
                

                body: JSON.stringify({
                    numero_comprobante: Numero_C,
                    fecha_cierre: Fecha_C,
                    correo: Correo_C,                 
                })        
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error: No se pudo confirmar la declaración');
                }                
                return response.json();
            })
            .then(data => {
                // indica que el dato llego bien     si es response es ok 
                Swal.fire({
                    title: "¡Actualizado !",
                    text: "Su registro fue actualizado.",
                    icon: "success"
                });
                // recarga la pagina 
                location.reload();  
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

// Visor de las declaraciones Confirmadas Cerradas y en historico carga de datos 
function StDeclaracionesConfirmadasCerradasHistoricas(){
    fetch(`/VerDeclaracionHistoricasCerradas/`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Error: No se pueden mostrar los datos');
        }
        return response.json();
    })
    .then(datadeclaracion => {
        const tbody = document.querySelector("tbody");
        tbody.innerHTML = '';

        datadeclaracion.forEach(item => {
            const row = document.createElement("tr");
            const fechaProxima = new Date(item.Fecha_Presenta);
            const fechaAsignada = new Date(item.Fecha_Asigna);
            const fechaActual = new Date(); // fecha actual
            const diffTiempo = fechaProxima.getTime() - fechaActual.getTime();
            const diffDias = Math.ceil(diffTiempo / (1000 * 60 * 60 * 24));

            let diasRestantesHTML = `<td>${diffDias} días</td>`; // Calcula días restantes                                                          

            row.innerHTML = `
                <td>${item.IDHistorico_Declaraciones}</td>
                <td>${item.IDDeclaracion__codigo}</td>                
                <td>${item.IDClientes_Proveedores__IDClientes_Proveedores}</td>
                <td>${item.IDClientes_Proveedores__Descripcion}</td>
                <td>${formatDate(item.Fecha_Asigna)}</td>
                <td>${formatDate(item.Fecha_Presenta)}</td>
                <td>${formatDate(item.Fecha_Cierre)}</td>                          
                <td>${item.IDPlanilla_Funcionarios__Nombre}</td>              
                <td>${item.IDDeclaracion__estado ? "A" : "I"}</td>  
                <td>${item.correo ? "Si" : "No"}</td>                        
                <td>${item.Numero_Comprobante}</td>                
                <td>${item.Fecha_Final}</td> `
          
            tbody.appendChild(row);

        });       
    })
    .catch(error => {
        console.error('Error al obtener los datos:', error);
    });
}

// busca la fecha seleccionada 
function StBuscaporfecha(){       
    var fechaSeleccionada = document.getElementById("fecha").value;
    fechaf=formatDate(fechaSeleccionada)
    console.log('fecha',fechaSeleccionada)
    fetch(`/Buscaporfecha/${fechaSeleccionada}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('No se encuentran datos correctos ');
        }
        return response.json(); // o response.text() si esperas otro tipo de respuesta
      })      
        .then(datadeclaracion => {
            const tbody = document.querySelector("tbody");
            tbody.innerHTML = '';
    
            datadeclaracion.forEach(item => {
                const row = document.createElement("tr");                            
                row.innerHTML = `
                    <td>${item.IDCalendario_tributario}</td>
                    <td>${item.IDDeclaracion__codigo}</td>                
                    <td>${item.IDDeclaracion__detalle}</td>
                    <td>${item.IDDeclaracion__tiempo}</td>
                    <td>${item.IDDeclaracion__observaciones}</td>                    
                    <td><a name="" id="" class="btn btn-danger"  href="#" onclick="Stborralineacalendario(${item.IDCalendario_tributario})" role="button">Eliminar</a></td>  `

                tbody.appendChild(row);
            });                       
      })
      .catch(error => {
        console.error('Fetch error:', error);
      });
    }


// Este es el boton de Calendario Tributario que agrega las declaraciones a la fecha especifica
function Stagrega_Declaracion(){
    // obtiene la declaracion seleccionada 
    var declaracion_seleccionada = document.getElementById('lcalendario').value;
    // obtiene la fecha seleccionada 
    var fecha_selecionada = document.getElementById('fecha').value;    

    //const formato_fecha_seleccionada = formatDate(fecha_selecionada);
    
    const data = {
        fecha_Presenta: fecha_selecionada ,
        Observaciones : 'N/A',
        IDDeclaracion: declaracion_seleccionada,
     };       

    fetch(`/AgregaDeclaracionCalendario/${fecha_selecionada}`, {            
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()           
        },
        body: JSON.stringify(data),
    })        
    .then(response => {      
      
        if (data) {
            console.log('respuesta',response)  
            swal.fire("Excelente!", "Nueva declaración Agregada.", "success");            
            // Recarga datos    
            //location.reload();     
            StBuscaporfecha();
        } else {
            swal.fire("Oops!", "Nueva declaración no incluida. Verifique si ya la agrego y esta tratando de agregarla nuevamente.", "error");             
        }
    })
    .catch(error => {
        swal.fire("Oops!", "Posiblemente ya este incluida la declaración.", "error");               
    });
} 


//elimina una linea asignada al calendario tributario 
function Stborralineacalendario(id){       
     fetch(`/BorraCalendarioLinea/${id}`,{            
         method: 'POST',
         headers: {
             'Content-Type': 'application/json',
             'X-CSRFToken': getCSRFToken()           
         },        
     })         
     .then(response => {             
         if (!response.ok) {
            swal.fire("Error!", "No se puedo eliminar la linea de declaración.", "error");                          
         } 
         return response.json();
     })
     .then(data=> {
        swal.fire("Excelente!","Elimando correctamente.","success");
        StBuscaporfecha();
     })
     .catch(error => {
             swal.fire("Oops!", "No se puedo eliminar la linea de declaración2.", "error");                   
     });
} 

// Función para mostrar u ocultar el calendario
function toggleCalendar() {
    var calendar = document.getElementById('calendar');
    calendar.style.display = (calendar.style.display === 'block') ? 'none' : 'block';
}

// Función para generar el calendario de meses y años
function generateCalendar() {
    var calendar = document.getElementById('calendar');
    calendar.innerHTML = ''; // Limpiar contenido anterior

    // Array de meses (puedes personalizarlos según tus necesidades)
    var months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

    // Año actual y años pasados y futuros
    var currentYear = new Date().getFullYear();
    var yearsToShow = 10; // Mostrar 10 años hacia atrás y 10 años hacia adelante

    // Generar botones para cada mes y año
    for (var i = currentYear - yearsToShow; i <= currentYear + yearsToShow; i++) {
        months.forEach(function(month, index) {
            var monthButton = document.createElement('button');
            monthButton.textContent = month + ' ' + i;
            monthButton.classList.add('month-button');
            monthButton.addEventListener('click', function() {
                // Aquí puedes manejar la selección del mes y año
                var selectedDate = (index + 1) + '/' + i; // Formato MM/YYYY
                document.getElementById('fecha').value = selectedDate;
                toggleCalendar(); // Ocultar el calendario después de seleccionar
            });
            calendar.appendChild(monthButton);
        });
    }

    // Puedes agregar más personalización o lógica según tus necesidades
}

// Muestra solo años se esta utilizando en Calendario Tributario

function StbuscaDeclaracionesCalendarioanual(anSeleccionada){
  // var anSeleccionada = document.getElementById("selector-a").value;  
    fetch(`/Buscadeclaracionxan/${anSeleccionada}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('No se encuentran datos correctos ');
        }        
        return response.json(); // 
      })      
        .then(datadeclaracion => {
            const tbody = document.querySelector("tbody");
            tbody.innerHTML = '';
    
            datadeclaracion.forEach(item => {
                const row = document.createElement("tr");                            
                row.innerHTML = `
                    <td>${item.IDCalendario_tributario}</td>
                    <td>${item.IDDeclaracion__codigo}</td>                
                    <td>${item.IDDeclaracion__detalle}</td>                    
                    <td>${item.Fecha_Presenta}</td>`
                          

                tbody.appendChild(row);
            });               
      })
      .catch(error => {
        console.error('Fetch error:', error);
      });

}
