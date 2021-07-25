$("#runPlayerService").click(function() {
    $.ajax({
        url: "/api/player/",
        // shows the loader element before sending.
        beforeSend: function() {
            $("#runPlayerService").hide();
            $("#playerServiceSpinner").show();
        },
        // hides the loader after completion of request, whether successfull or failor.
        complete: function() {
            $("#playerServiceSpinner").hide();
            $("#runPlayerService").show();
        },
        success: function(data) {
            $("#playerServiceSuccess").show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#playerServiceError").show();
        },
        type: 'GET',
    })
});

$("#runPlayerAttributeService").click(function() {
    $.ajax({
        url: "/api/player/attributes/",
        // shows the loader element before sending.
        beforeSend: function() {
            $("#runPlayerAttributeService").hide();
            $("#playerAttributeServiceSpinner").show();
        },
        // hides the loader after completion of request, whether successfull or failor.
        complete: function() {
            $("#playerAttributeServiceSpinner").hide();
            $("#runPlayerAttributeService").show();
        },
        success: function(data) {
            $("#playerAttributeServiceSuccess").show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#playerAttributeServiceError").show();
        },
        type: 'GET',
    })
});

//Alert should be able to reappear (BS will remove it after first close)
$(function() {
   $(document).on('click', '.close', function() {
       $(this).parent().hide();
   })
});