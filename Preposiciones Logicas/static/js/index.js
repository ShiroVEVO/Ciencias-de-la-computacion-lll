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
            console.log("La respuesta no es un JSON AhHhHhH");
        }
    }).catch((error) =>{
        console.log("Hubo un error con la petición Fetch en RESPONSE" + error);
    }).then((data) => {
        document.getElementById("solucion").style.display = "flex";
        mensaje = "<h3>Solución</h3>Preposición:<b> " + data["tabla"] + "</b><br>"
        mensaje += "<p>Variables: <b>"+data["variables"]+"</b></p>";
        mensaje += "<p>Parentesis: <b>"+data["parentesis"]+"</b></p>";
        mensaje += "<p>Operadores: <b>"+data["operadores"]+"</b></p>";
        if(data["valoracion"]=='Tautology')
            null;//mensaje += "<p><b>Tatuología</b></p>";
        else if(data["valoracion"]=='Contingency')
            null;//mensaje += "<p><b>Contingencía</b></p>";
        else if(data["valoracion"]=='Contradiction')
            null;//mensaje += "<p><b>Contradicción</b></p>";
        document.getElementById('solucion').innerHTML = mensaje
    }).catch((error) =>{
        document.getElementById("solucion").style.display = "flex";
        mensaje = "<b>Preposición invalida</b>";
        document.getElementById('solucion').innerHTML = mensaje
    })
})