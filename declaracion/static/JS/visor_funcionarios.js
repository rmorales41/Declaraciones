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
  
  
  