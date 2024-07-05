// Calendario Tributario Reasignacion de fechas para definir nuevas fechas para el control del proximo año  <td><input type="date" id="fecha_propuesta_${item.IDCalendario_Tributario}" name="fecha_propuesta" value="${sumarDias(item.Fecha_Presenta, item.declaracion__tiempo)}"></td>`
function StbuscaDeclaracionesCalendariomensual(selectedYear,selectedMonth){  
    // var anSeleccionada = document.getElementById("selector-a").value;  
      fetch(`/Buscadeclaracionxm/${selectedYear},${selectedMonth}/`)
        .then(response => {
          if (!response.ok) {
            throw new Error('No se encuentran datos correctos ');
          }        
          return response.json(); // 
        })        
          .then(datadeclaracion => {
              const tbody = document.querySelector("tbody");
              tbody.innerHTML = '';              
              datadeclaracion.forEach(item => {
                  const row = document.createElement("tr");  
                  
                // Asigna IDDeclaracion__IDDeclaracion como un atributo en la fila
                row.setAttribute('data-iddeclaracion', item.IDDeclaracion__IDDeclaracion);

                  row.innerHTML = `
                      <td>${item.IDCalendario_tributario}</td>
                      <td>${item.IDDeclaracion__codigo}</td>                
                      <td>${item.IDDeclaracion__detalle}</td>                    
                      <td>${formatDate(item.Fecha_Presenta)}</td>
                      <td><input type="date" id="fecha_propuesta_${item.IDCalendario_Tributario}" name="fecha_propuesta" value="${sumarUnAnio(item.Fecha_Presenta)}"></td>
                      `
  
                  tbody.appendChild(row);
              });               
        })
        .catch(error => {
          console.error('Fetch error:', error);
        });
  
  }
  

  // cambia el formato de la fecha que se observa a dd/mm/yyyy
  function formatDate(dateString) {  
    // Extrae el día, mes y año    
    const date = moment(dateString); 

    const day = date.date();
    const month = date.month() + 1; // getMonth devuelve 0 para enero, por eso se suma 1
    const year = date.year();

    // Asegura dos digitos 
    const formattedDay = day < 10 ? '0' + day : day;
    const formattedMonth = month < 10 ? '0' + month : month;    

    // Retorna la fecha formateada en formato dd/mm/yyyy
    return `${formattedDay}-${formattedMonth}-${year}`;
}


// suma los dias a la fecha de presentacion 
function sumarUnAnio(fecha) {
  const fechaActual = new Date(fecha); // Convertir la fecha a objeto Date
  const resultado = new Date(fechaActual); // Crear una nueva fecha para no modificar la original
  resultado.setFullYear(fechaActual.getFullYear() + 1); // Sumar un año
  
  // Formatear la fecha en formato "YYYY-MM-DD" para que sea compatible con <input type="date">
  const formattedDate = resultado.toISOString().slice(0, 10);

  return formattedDate;
}

// obtiene la declaracion seleccionada 
function StguardaReasignacion(){
  
    var tbody = document.querySelector("tbody");
    var rows = tbody.querySelectorAll("tr");

    // Iterar sobre las filas de la tabla para verificar y enviar datos
    rows.forEach(row => {
        // Obtener el input de fecha propuesta de la fila actual
        let inputFecha = row.querySelector(`input[name="fecha_propuesta"]`);        
        // Obtener el valor de la fecha propuesta
        var fecha_propuesta = inputFecha.value;        
                  
        if (fecha_propuesta) {
            // Obtener IDDeclaracion__IDDeclaracion desde el atributo de la fila
            var IDD = row.getAttribute('data-iddeclaracion');

            // Procesar la fecha propuesta si necesitas enviarla a través de fetch 
            //var declaracion_seleccionada = document.getElementById('selector-a').value;                    
            const data = {
                fecha_Presenta: fecha_propuesta,
                Observaciones: 'N/A',
                iddeclaracion: parseInt(IDD), // convierte a entro si es necesario
            };                   

            fetch(`/ReasignaDeclaracionCalendario/${fecha_propuesta}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify(data),
                })
                .then(response => {
                    if (response.ok) {
                        swal.fire("Excelente!", "Nueva declaración Agregada.", "success");                     
                    } else {
                        swal.fire("Oops!", "Nueva declaración no incluida. Verifique si ya la agregó y está tratando de agregarla nuevamente.", "info");
                    }
                })
                .catch(error => {
                    swal.fire("Oops!", "Posiblemente ya está incluida la declaración.", "error");
                });
        } else {
            swal.fire("Error!", "Debe seleccionar una fecha propuesta.", "error");
        }
    });
}

// Función para obtener el token CSRF
function getCSRFToken() {
  const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
  return csrfTokenElement ? csrfTokenElement.value : null;
}
