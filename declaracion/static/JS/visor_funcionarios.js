// busca agentes
function StVisorFuncionario() {
    fetch(`/VisorFuncionario/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('No se logró la consulta : ' + response.statusText);
            }
            return response.json();
        })
        .then(datos_conteo  => {
          // limpiar la tabla Datatables
            var table = $('#visorfuncionarios').DataTable();
            table.clear().draw();
            // Iterar sobre los datos obtenidos y agregar filas a DataTables
            datos_conteo .forEach(item => { 
                console.log('llego',item)            
              table.row.add([
                  item.IDPlanilla_Funcionarios,
                  item.IDPlanilla_Funcionarios__Nombre ,
                  item.total_asignaciones,
              ]).draw(false); // draw(false) para evitar renderizado repetido
          });
      })
      .catch(error => {
          console.error('Fetch error:', error);
      });
  }
  
  
// Carga el select del funcionario 
function StListacolaboradores(){    
    let select = document.getElementById("funcionarios");
    // Limpia cualquier opción existente
    select.innerHTML = '';    
    fetch(`/ListaColaboradores/`)
    .then(response => {
        if (!response.ok) {
            throw new Error('No se logró la consulta : ' + response.statusText);
        }
        return response.json();
    })
    .then(datos  => {
        datos.forEach(datos => {
            let option = document.createElement('option');
            option.value = datos.IDPlanilla_Funcionarios
            option.textContent = datos.Nombre 
            option.setAttribute('data-estado',datos.Estado)       
            select.appendChild(option);
        });
    })
}
 
// busca los clientes asignados al colaborador 
function Stbuscaclientesasignados(IDD){        
    fetch(`/DetalleColaborador/${IDD}/`)
    .then(response => {
        if (!response.ok){
             throw new Error('No se logro la consulta' + response.statusText);
        }
        return response.json();       
    })
    .then(datos => {
        // limpiar la tabla Datatables
        var table = $('#visorasginados').DataTable();
        table.clear().draw();
        // Iterar sobre los datos obtenidos y agregar filas a DataTables    
        datos .forEach(item => { 
            
            table.row.add([
              item.IDClientes_Proveedores__IDClientes_Proveedores,
              item.IDClientes_Proveedores__Descripcion ,  
              item.IDClientes_Proveedores__Direccion,            
              item.IDClientes_Proveedores__Fecha_Ult_Movimiento
          ]).draw(false); // draw(false) para evitar renderizado repetido
        })
    }) 
}

// Muestra la lista de clientes Funcionarios 
function StListaClientesFuncionarios(){
    fetch(`/DetalleClienteColaborador/`)
    .then(response => {
        if (!response.ok){
             throw new Error('No se logro la consulta' + response.statusText);
        }
        return response.json();       
    })
    .then(datos => {
        // limpiar la tabla Datatables
        var table = $('#visorasginados').DataTable();
        table.clear().draw();
        // Iterar sobre los datos obtenidos y agregar filas a DataTables   
        datos .forEach(item => {          
            console.log(item)         
            table.row.add([
              item.IDClientes_Proveedores,
              item.Descripcion ,                
              item.Fecha_Ult_Movimiento,  
              `<td>${item.asignado ? "Asignado" : "Sin Asignar"}</td>`
          ]).draw(false); // draw(false) para evitar renderizado repetido
        })
    }) 
}

   