entrada = document.getElementById("entrada")
formulario = document.getElementById("formulario")

function agregar(char) {
    premisa = entrada.value + char
    console.log(premisa)
    entrada.value = premisa
    //alert(char);
}
function borrarUltimo(){
    premisa = entrada.value
    entrada.value = premisa.substr(0,premisa.length -1)
    console.log(entrada.value)
}

formulario.addEventListener('submit', e=>{
    //console.log("submit");
    e.preventDefault();

    const data = new FormData();
    data.append('prep', document.getElementById('entrada').value);
    
    fetch('solvePreposition', {
        method: 'POST',
        mode: 'cors',
        body: data
    }).then((response) =>{
        var contentType = response.headers.get('content-type');
        if(contentType && contentType.indexOf("application/json") !== -1){
            return response.json();
        } else {
            console.log("La respuesta no es un JSON perro");
        }
    }).catch((error) =>{
        console.log("Hubo un error con la petición Fetch en RESPONSE" + error);
    }).then((data) => {
        //console.log(data)
        document.getElementById("solucion").style.display = "flex";
        mensaje = "<h3>Solución</h3><br>" + data["tabla"] + "<br>"
        if(data["valoracion"]=='Tautology')
            mensaje += "<p><b>Tatuología</b></p>";
        else if(data["valoracion"]=='Contingency')
            mensaje += "<p><b>Contingencía</b></p>";
        else if(data["valoracion"]=='Contradiction')
            mensaje += "<p><b>Contradicción</b></p>";
        //console.log(mensaje);
        //alert("Se agrego "+ document.getElementById("name").value);
        document.getElementById('solucion').innerHTML = mensaje
        //location.reload();
    }).catch((error) =>{
        console.log("Hubo un error con la petición Fetch en DATA" + error);
    })
})