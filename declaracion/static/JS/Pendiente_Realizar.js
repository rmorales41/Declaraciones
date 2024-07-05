// Busca las declaraciones del mes y los clientes pendientes 

function StCalendariomensual(selectedYear, selectedMonth) {
    // Lógica para obtener datos de declaraciones y luego actualizar la tabla DataTables 
    //console.log('llegue st',selectedYear, selectedMonth)   
      // Obtén el elemento <select> por su ID
      //let select = document.getElementById("ldeclaraciones");
      // Limpia cualquier opción existente
      //select.innerHTML = '';
      // Hace la consulta al url para ejecutar la vista 
      fetch(`/Realizar_consulta/${selectedYear},${selectedMonth}/`)
      .then(response => {                     
          if (!response.ok) {
              throw new Error('No se logró la consulta : ' + response.statusText);
          }
          // convierte la respuesta en json <td><a name="" id="" class="btn btn-secondary" href="#" onclick="Stfinaliza(${item.IDHistorico_Declaraciones})">Finalizar</a></td>
          return response.json();
            })
      .then(datadeclaracion => {
        const tbody = document.querySelector("tbody");
        tbody.innerHTML = '';
        datadeclaracion.forEach(item => {
            const row = document.createElement("tr");                                      
            row.innerHTML = `                        
                <td>${item.IDDeclaracion}</td>
                <td>${item.IDDeclaracion__codigo}</td>                
                <td>${item.IDDeclaracion__detalle}</td>                
                <td>${item.IDDeclaracion__asignacion__IDAsignacion}</td> 
                <td>${item.IDDeclaracion__asignacion__IDClientes_Proveedores__Descripcion}</td>               
                <td>${item.IDDeclaracion__asignacion__Fecha_Asigna}</td> 
                <td>${item.IDDeclaracion__asignacion__Fecha_Proxima}</td>
                <td>${item.IDDeclaracion__asignacion__IDPlanilla_Funcionarios__Nombre}</td>          
                `;
            tbody.appendChild(row);
        });               
  })
  .catch(error => {
    console.error('Fetch error:', error);
  });

}
         









