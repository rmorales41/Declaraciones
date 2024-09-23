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
    // Redirigir 
    window.location.href = "/editar_tipo/" + idTipo;
}

// boton guarda registro tipo 
function StguardaRegistro() {        
    window.location.href = "/guarda_tipo/" ;
}

// busca todos los beneficios que tiene el cliente 
function StBuscaBeneficios(IDD){        
        fetch(`/busca_beneficios/${IDD}`)
        .then(response => {
         if (!response.ok) {
                throw new Error('No se logró la consulta : ' + response.statusText);
                      }
            return response.json();
        })

        .then(datos => {        
        // limpiar la tabla Datatables             
        var table = $('#visortipos').DataTable();
        table.clear().draw();

            // Iterar sobre los datos obtenidos y agregar filas a DataTables
            datos.forEach(item => {
                const fechaMov = formatearFecha(item.Fecha_vencimiento);                   
                 // Crear el elemento con ambos botones
                const acciones = `
                    <div class="acciones" role="group">
                        <button type="button" class="btn btn-primary btn-editar" data-id="${item.IDDetalle_Declaracion_Tipo}">
                            <i class="bi bi-pencil"></i></button>
                    
                         <button type="button" class="btn btn-danger btn-eliminar" data-id="${item.IDDetalle_Declaracion_Tipo}">
                            <i class="bi bi-trash"></i></button>
                    </div>
                            `;             
                
                table.row.add([
                    item.IDDetalle_Declaracion_Tipo,
                    item.IDDeclaraciones_Tipo__Descripcion,
                    item.Detalle,
                    item.Numero_solicitud,
                    item.Numero_autorizado,
                    fechaMov ,
                    item.Estado ? "Si" : "No" ,                    
                    acciones                    
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

