function validar(valor) {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    var aux = valor;

    if (aux <= 0) {
        alert("El valor debe ser mayor a 0");
    }
}

function validar_text(valor) {

    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    var aux = valor;
    if (aux == '' || aux == undefined) {
        alert("falta llenar campo");
    }
}