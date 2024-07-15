function StVisorClientes(){   
    fetch(`/VisorClientes/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('No se logró la consulta : ' + response.statusText);
            }
            return response.json();
        })
        .then(datos  => {
          // limpiar la tabla Datatables
            var table = $('#visorclientes').DataTable();
            table.clear().draw();
            // Iterar sobre los datos obtenidos y agregar filas a DataTables
            datos .forEach(item => {     
                console.log(item)                    
              table.row.add([
                  item.IDClientes_Proveedores,
                  item.Descripcion ,
                  item.Direccion,
                  item.Email,
                  item.Fecha_Ult_Movimiento,
              ]).draw(false); // draw(false) para evitar renderizado repetido
          });
      })
      .catch(error => {
          console.error('Fetch error:', error);
      });
  }
  
  