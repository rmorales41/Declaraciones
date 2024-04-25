//<!-- https://www.youtube.com/watch?v=qgf0UYzL5BY -->
//  alert("UskokruM2010 - prueba");
// cuando se carga se agrega un escuchador al formulario y que espere por la funcion carga

const listarClientes = async() => {
  
    try{
        // permite hace peticiones asincronas 
        const response = await fetch("/asigna");
        const data = await response.json();
        
        if(data.message == "Success") {
            let opciones = ``;
            data.clientes.forEach((cliente_proveedor_cliente_proveedor) => {
                opciones +=`<option value = '${cliente_proveedor_cliente_proveedor.IDClientes_Proveedores}'>${
                    cliente_proveedor_cliente_proveedor.Descripcion}</option>`;
            });
            // llenado del combo de lista de funcionarios         
            ListClient.innerHTML = opciones ;            
        }else {
            alert("No se pudo cargar");
        }
    }catch (error) {
        console.log(error);
};

};

// asicrono espera un proceso carga clientes 
const cargaInicial=async()=>{
    await listarClientes(); // Espera a que se carguen los clientes   
    // alert("UskokruM2010 - prueba"); 
    // cuando hay un cambio lo vuelve a llamar detenta cambios 
    ListClient.addEventListener("change", async()=> {
        console.log(event);
        console.log(event.target)
        console.log(event.target.value)

        await listarClientes();
    })
};


// cuando se carga se pone a escuchar sincrno y carga incial 
windows.addEventListener("load", async() =>{
    await cargaInicial();

});


document.querySelector('.form-select').addEventListener('change', async (event) => {
    await cargaInicial();
});
=======

// carga la lista de clientes por funcionario // 
function listarClientes() {
    // Elimina todas las opciones actuales       
    var selectElement = document.getElementById("clientes");
    // Obtener el valor seleccionado (nombre del funcionario)
    var selectedValue  = selectElement.options[selectElement.selectedIndex].value;
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
    // limpia select 
    Clientfunc.innerHTML="";
   // console.log("Carga clientes funcionario:",idd); 
    
    try {
        const response = await fetch(`/asignaciones/${idd}`);
        const data = await response.json();           
     //   console.log(data)
        if (data && data.data && data.data.length > 0) {
            const select = document.getElementById("Clientfunc");
            
            data.data.forEach(item => {
                const option = document.createElement("option");
                option.value = item.IDClientes_Proveedores_id;
                option.textContent = item.Descripcion;
                select.appendChild(option);

             // var idfunc = selectedOption.IDPlanilla_Funcionarios_id   
             // console.log('Pase por aqui',IDCliente_Proveedores_id);              

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
    // limpia select     
    //  Clientfunc.innerHTML="";

     //  console.log("Carga Declaracion Clientes :",idd)

    try {
           const response = await fetch(`/declaracionxcliente/${idd}`);
           const data = await response.json();     

           
          // console.log(data)

           if (data.length > 0) {
            //   const select = document.getElementById("Clientfunc");
           // console.log('Carga Declaracion Clientes',data)      
            const tbody = document.querySelector("tbody");
            tbody.innerHTML = ""; // Limpiar tbody antes de agregar nuevas filas
             
                data.forEach(declaracion => {
                    console.log('entrar a forEach')
                    console.log(declaracion.codigo)
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${declaracion.iddeclaracion}</td>
                    <td>${declaracion.codigo}</td>
                    <td>${declaracion.detalle}</td>
                    <td>${declaracion.presentada}</td>
                    <td>${declaracion.asignada}</td>  
                    <td scope="row" style="color: ${declaracion.correo ? 'black' : 'red'}">${declaracion.correo ? 'Enviado' : 'No Enviado'}</td>                                        
                    `;
                     tbody.appendChild(row);
                   });
           } else {
               console.error("Atención no se encontraron datos de declaraciones asignadas.");
           }           
    } catch (error) {
        console.error("Error en la solicitud:", error);
    }
} 

async function Clientessinasignacion() {
      var asignaDeclaracionURL = "/asigna_declaracion/";      
      var select = document.getElementById("clientepend");       // obtiene el elemento del select 
      var selectedOption = select.options[select.selectedIndex]; // obtiene el indice de la opcion seleccionada      
      var selectedClientId = selectedOption.value;               // obtiene el valor   
      var select = document.getElementById("clientes");          // obtiene el elemento de colaboradores  
      var selectedOption = select.options[select.selectedIndex]; // obtiene el indice de la opcion seleccionada
      var selectedColaboradorId = selectedOption.value;          // obtiene el valor del funcionario                   

      console.log('Entre a clientes asignacion',selectedClientId)
      console.log('Entre a clientes asignacion',selectedColaboradorId)
      
      window.location.href = asignaDeclaracionURL + selectedClientId + "/" + selectedColaboradorId ; // Redirecciona a la vista y pasa dos parametros 
  }

