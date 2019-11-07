function funcion2(x) {

    $.ajax({
        xhrFields: {
            withCredentials: false
        },
        dataType: 'text',
        url: "./formulario_componente_ms?id=" + x,
        success: function(obj) {
            console.log(obj.id);
            $('.mf-prueba').html(obj);
            alert(x);
        },
        error: function(objeto, quepaso, otroobj) {
            console.log(quepaso);
        }
    });

}