// Muesta la lista de los tipos de declaraciones pyme, etc Uso con datatable
/* function StVisorMantenimiento_old(){
    fetch(`/VisorTipos/`)
    .then(response => {
        if (!response.ok) {
            throw new Error('No se logró la consulta : ' + response.statusText);
        }
        return response.json();
    })
    .then(datos  => {
      // limpiar la tabla Datatables
        var table = $('#visormantenimiento').DataTable();
        table.clear().draw();
        // Iterar sobre los datos obtenidos y agregar filas a DataTables
        datos .forEach(item => {                                     
          table.row.add([
              item.IDDeclaraciones_Tipo,
              item.Descripcion ,
              item.Institucion,
              item.Observacion,
            `<td>${item.Estado ? "Activo" : "Inactivo"}</td>`,            
          ]).draw(false); // draw(false) para evitar renderizado repetido
      });
  })
  .catch(error => {
      console.error('Fetch error:', error);
  });
} */

// Tipos de Declaracion con visor normal 
function StVisorMantenimiento() {
    fetch(`/VisorTipos/`)
    .then(response => {
        if (!response.ok) {
            throw new Error('No se logró la consulta : ' + response.statusText);
        }
        return response.json();
    }).then(datos => {
        const tbody = document.querySelector("tbody");
        tbody.innerHTML = '';

        datos.forEach(item => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${item.IDDeclaraciones_Tipo}</td>
                <td>${item.Descripcion}</td>                
                <td>${item.Institucion}</td>
                <td>${item.Observacion}</td>                        
                <td>${item.Estado ? "Activo" : "Inactivo"}</td>                                        
                <td> 
                    <a class="btn btn-primary" href="#" onclick="editar(${item.IDDeclaraciones_Tipo})" role="button">
                        <i class="fas fa-edit"></i>
                    </a>  
                    <a class="btn btn-danger" href="#" onclick="eliminatipo(${item.IDDeclaraciones_Tipo})" role="button">
                        <i class="fas fa-trash-alt"></i>
                    </a>
                </td>`;
            
            tbody.appendChild(row);
        });

        console.log(datos);
    }).catch(error => {
        console.error('Error en la solicitud fetch:', error);        
    });
}


// Elimina tipo de Beneficio 
function eliminatipo(IDD) {
    console.log('eliminando ');
    Swal.fire({
        title: "Desea Eliminar este Tipo",
        text: "Recuerde que si tiene documentos ligados no podrá eliminarla.",
        icon: "warning",
        showCancelButton: true,
        cancelButtonText: "No, Cancelar",
        confirmButtonText: "Si, Eliminar",
        reverseButtons: true,
        confirmButtonColor: "#dc3545",
        backdrop: true,
        showLoaderOnConfirm: true,  
    }).then(function(result) {
        if (result.isConfirmed) {                    
            window.location.href = "/elimina_tipo/" + IDD;
        }
    });
}

// Función para editar tipo
function editar(idTipo) {      
    // Redirigir o hacer lo que necesites con la URL    
    window.location.href = "/editar_tipo/" + idTipo;
}
 
