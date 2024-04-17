//<!-- https://www.youtube.com/watch?v=qgf0UYzL5BY -->
//  alert("UskokruM2010 - prueba");
// cuando se carga se agrega un escuchador al formulario y que espere por la funcion carga

const listarClientes = async() => {
  
    try{
        // permite hace peticiones asincronas 
        const response = await fetch("/asigna");
        const data = await response.json();
        
        if(data.message == "Success") {
            let opciones = ``;
            data.clientes.forEach((cliente_proveedor_cliente_proveedor) => {
                opciones +=`<option value = '${cliente_proveedor_cliente_proveedor.IDClientes_Proveedores}'>${
                    cliente_proveedor_cliente_proveedor.Descripcion}</option>`;
            });
            // llenado del combo de lista de funcionarios         
            ListClient.innerHTML = opciones ;            
        }else {
            alert("No se pudo cargar");
        }
    }catch (error) {
        console.log(error);
};

};

// asicrono espera un proceso carga clientes 
const cargaInicial=async()=>{
    await listarClientes(); // Espera a que se carguen los clientes   
    // alert("UskokruM2010 - prueba"); 
    // cuando hay un cambio lo vuelve a llamar detenta cambios 
    ListClient.addEventListener("change", async()=> {
        console.log(event);
        console.log(event.target)
        console.log(event.target.value)

        await listarClientes();
    })
};


// cuando se carga se pone a escuchar sincrno y carga incial 
windows.addEventListener("load", async() =>{
    await cargaInicial();

});


document.querySelector('.form-select').addEventListener('change', async (event) => {
    await cargaInicial();
});
