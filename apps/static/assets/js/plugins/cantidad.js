function envio_datos(pc_nid,csrf_token) {
    // const pc_nid = pc_nid
    const cantidad = $("cantidad").val();
    console.log(csrf)
    $.ajax({
        url: "sy-envio_datos",
        method: "POST",
        data: {
            cantidad,
            pc_nid,
            csrfmiddlewaretoken:  csrf_token 
        },
        success: function (response) {
            location.reload();
        }

    })


}
