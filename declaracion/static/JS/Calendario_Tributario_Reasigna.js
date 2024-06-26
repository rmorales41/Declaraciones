// Calendario Tributario Reasignacion 
function StbuscaDeclaracionesCalendarioanual(anSeleccionada){
    // var anSeleccionada = document.getElementById("selector-a").value;  
      fetch(`/Buscadeclaracionxan/${anSeleccionada}/`)
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
                  row.innerHTML = `
                      <td>${item.IDCalendario_tributario}</td>
                      <td>${item.IDDeclaracion__codigo}</td>                
                      <td>${item.IDDeclaracion__detalle}</td>                    
                      <td>${item.Fecha_Presenta}</td>`
                            
  
                  tbody.appendChild(row);
              });               
        })
        .catch(error => {
          console.error('Fetch error:', error);
        });
  
  }
  