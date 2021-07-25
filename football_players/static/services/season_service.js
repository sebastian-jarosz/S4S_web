$("#runSeasonService").click(function() {
    $.ajax({
        url: "/api/season/",
        // shows the loader element before sending.
        beforeSend: function() {
            $("#runSeasonService").hide();
            $("#seasonServiceSpinner").show();
        },
        // hides the loader after completion of request, whether successfull or failor.
        complete: function() {
            $("#seasonServiceSpinner").hide();
            $("#runSeasonService").show();
        },
        success: function(data) {
            $("#seasonServiceSuccess").show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#seasonServiceError").show();
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