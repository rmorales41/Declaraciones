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
  