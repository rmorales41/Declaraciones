// busca movimientos historicos busqueda 
function StMovimientohistorico() {
            fetch(`/Historicomovimientosbuscar/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('No se logró la consulta : ' + response.statusText);
                    }
                    return response.json();
                })
                .then(tmovimientos => {
                // limpiar la tabla Datatables
                    var table = $('#declaracionesTabla').DataTable();
                    table.clear().draw();
        
                    // Iterar sobre los datos obtenidos y agregar filas a DataTables
                    tmovimientos.forEach(item => {
                    const fechaMov = formatearFecha(item.Fecha_Asigna);
                    const fechapres = formatearFecha(item.Fecha_Presenta);
                    const fechaFinalFormateada = formatearFecha(item.Fecha_Final);
                    table.row.add([
                        item.IDHistorico_Declaraciones,
                        item.IDDeclaracion__codigo,
                        item.IDDeclaracion__detalle,
                        item.IDClientes_Proveedores__Descripcion,
                        fechaMov ,
                        fechapres,
                        fechaFinalFormateada,
                        item.Numero_Comprobante,
                        item.IDPlanilla_Funcionarios__Nombre
                    ]).draw(false); // draw(false) para evitar renderizado repetido
                });
                
            })
            
            .catch(error => {
                console.error('Fetch error:', error);
            });
    }
  
  // formatear fecha 
  function formatearFecha(fechaCompleta) {
    const fecha = new Date(fechaCompleta);
    const dia = fecha.getDate();
    const mes = fecha.getMonth() + 1;
    const anio = fecha.getFullYear();
  
    // Formato deseado: dd/mm/yyyy
    const fechaFormateada = `${dia}/${mes}/${anio}`;
  
    return fechaFormateada;
  }
  

  // datos de clientes en los estados 
  function StListaclientesEstado() {            
    let select = document.getElementById("ListaClientes");          // define el combo para mostrar datos
    if (select){
            fetch('/ListaclientesDeclaracion/')
                .then(response => {
                    // Verifica si la respuesta es OK (status 200-299)
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json(); // Parsear la respuesta JSON
                })
                .then(responseData => {                  
                    if (responseData.data && responseData.data.length > 0) {
                        // Limpia las opciones anteriores si las hay
                        select.innerHTML = '';
                        responseData.data.forEach(item => {
                            const option = document.createElement("option");
                            option.value = item.IDClientes_Proveedores;
                            option.textContent = item.Descripcion;
                            select.appendChild(option);
                        });
                        datosCargados = true;
                    }
                    // Maneja el valor seleccionado solo después de cargar los datos
                    var selectedOption = select.options[select.selectedIndex];
                    var selectedClientId = selectedOption ? selectedOption.value : null;
                })
                .catch(error => {
                    console.error("Error en StListaclientesEstado:", error);
                });
        }
  }



// Busca las declaraciones asignadas al cliente en el historico solo de ese cliente 
  function StBuscaDeclaraciones(){         
     // optiene el valor del id     
     var clienteId = document.getElementById('ListaClientes');
     var seleccionclienteId = clienteId.value;       
     fetch(`/BuscaDeclaracionCliente/${seleccionclienteId}`) // busca la vista de datos 
     .then(response => {
        // Verifica si la respuesta es OK (status 200-299)
        if (!response.ok) {
                   throw new Error('Network response was not ok');
        }
               return response.json(); // Parsear la respuesta JSON
        })
        .then(tmovimientos=> {           
            // limpiar la tabla Datatables
            var table = $('#declaracionesTabla').DataTable();
            table.clear().draw();                                                 
            // Iterar sobre los datos obtenidos y agregar filas a DataTables
                tmovimientos.forEach(item => {
                        const fchprev = formatearFecha(item.Fecha_Presenta);
                        const fchsig  = formatearFecha(item.Fecha_Asigna);
                        const fchcie  = formatearFecha(item.Fecha_Cierre);
                        const fchfin   = formatearFecha(item.Fecha_Final);
                        const fchsys   = formatearFecha(item.Fecha_Sistema);
                        table.row.add([
                            item.IDHistorico_Declaraciones,
                            item.IDDeclaracion__codigo,                                            
                            item.IDClientes_Proveedores__Descripcion,
                            item.IDPlanilla_Funcionarios__Nombre,
                            fchprev,
                            fchsig ,
                            fchcie,
                            fchfin,
                            fchsys,
                            item.Numero_Comprobante,
                            item.rectificativa ? 'Si' : 'No',
                            item.Mes
                        ]).draw(false); // draw(false) para evitar renderizado repetido
                });
        })
        .catch(error => {
          console.error('Fetch error:', error);
        });
}
                        