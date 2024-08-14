function Buscaconcalendario(selectedYear,selectedMonth ) {           
    fetch(`/Buscaconcalendariofinal/${selectedYear},${selectedMonth}/`)
    .then(response => {
        if (!response.ok) {           
            throw new Error('No se logró la consulta : ' + response.statusText);
        }        
        return response.json();
    }).then(datos => {           
        const tbody = document.querySelector("#Tabla_Stat1 tbody"); //
        tbody.innerHTML = '';   
       
        datos.forEach(item => {                                               
            const row = document.createElement("tr");        
            // determina el color segun la condicion 
            const colorea = (item.IDHistorico_Declaraciones == null) ? '#F2D7D5' : 'white';            
       
            row.innerHTML = `                
                <td>${item.IDHistorico_Declaraciones}</td>
                <td>${item.IDDeclaracion__codigo}</td>
                <td>${item.IDClientes_Proveedores}</td>
                <td>${item.IDClientes_Proveedores__Descripcion}</td>
                <td>${item.IDPlanilla_Funcionarios__Nombre}</td>   
                <td>${item.Fecha_Presenta}</td>
                <td>${item.Fecha_Cierre}</td>
                <td>${item.Fecha_Final}</td>
                <td>${item.Fecha_Calendario}</td>
                <td>${item.Fecha_Sistema}</td>
                <td>${item.Numero_Comprobante}</td>                                
                <td>${item.rectificativa ? "Rectificativa" : "Normal"}</td>`;

              // Aplica el color al estilo de la fila
              //row.style.color = colorea;
              row.style.backgroundColor = colorea

            tbody.appendChild(row);
        });   

     // Reinicializar DataTable
        if ($.fn.DataTable.isDataTable('#Tabla_Stat1')) {
        $('#Tabla_Stat1').DataTable().clear().destroy(); // Destruir DataTable si ya está inicializado
       }
        
      $('#Tabla_Stat1').DataTable({
        "language": {
              "url": "{% static 'json/Spanish.json' %}"
          },
          "searching": true,  // Habilitar búsqueda global
          "ordering": true,   // Habilitar ordenamiento de columnas
          "paging": true ,    // Habilitar paginación
          "scrollX": true,    // Habilitar scroll horizontal
          "scrollY": "430px" // Altura del scroll vertical
       });

    }).catch(error => {
        console.error('Error en la solicitud fetch:', error);        
    });
}




