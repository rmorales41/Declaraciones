// 
function Buscaconcalendario(selectedYear,selectedMonth ) {

    console.log('llegue a la funcion ',selectedYear,selectedMonth)
    fetch(`/Buscaconcalendariog/${selectedYear},${selectedMonth}`)
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
