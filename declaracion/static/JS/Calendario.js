function Buscaconcalendario(selectedYear, selectedMonth) {           
    fetch(`/Buscaconcalendariofinal/${selectedYear},${selectedMonth}/`)
    .then(response => {
        if (!response.ok) {           
            throw new Error('No se logró la consulta : ' + response.statusText);
        }        
        return response.json();
    }).then(datos => {           
        const table = $('#Tabla_Stat1').DataTable();  // Obtiene instancia de DataTable
        table.clear();                                // Limpia la tabla existente
        
        datos.forEach(item => {                                               
            const colorea = (item.IDHistorico_Declaraciones == null) ? '#F2D7D5' : 'white';
            table.row.add([                
                item.IDHistorico_Declaraciones,
                item.IDDeclaracion__codigo,
                item.IDClientes_Proveedores,
                item.IDClientes_Proveedores__Descripcion,
                item.IDPlanilla_Funcionarios__Nombre,
                item.Fecha_Presenta,
                item.Fecha_Cierre,
                item.Fecha_Final,
                item.Fecha_Calendario,
                item.Fecha_Sistema,
                item.Numero_Comprobante,
                item.rectificativa ? "Rectificativa" : "Normal"
            ]).node().style.backgroundColor = colorea;               // Agrega fila y aplica el color
        });   

        table.draw();                                                // Redibuja la tabla para reflejar los nuevos datos
    }).catch(error => {
        console.error('Error en la solicitud fetch:', error);        
    });
}


