$("#runMatchService").click(function() {
    $.ajax({
        url: "/api/match/",
        // shows the loader element before sending.
        beforeSend: function() {
            $("#runMatchService").hide();
            $("#matchServiceSpinner").show();
        },
        // hides the loader after completion of request, whether successfull or failor.
        complete: function() {
            $("#matchServiceSpinner").hide();
            $("#runMatchService").show();
        },
        success: function(data) {
            $("#matchServiceSuccess").show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#matchServiceError").show();
        },
        type: 'GET',
    })
});

$("#runMatchEventService").click(function() {
    $.ajax({
        url: "/api/match/events/",
        // shows the loader element before sending.
        beforeSend: function() {
            $("#runMatchEventService").hide();
            $("#matchEventServiceSpinner").show();
        },
        // hides the loader after completion of request, whether successfull or failor.
        complete: function() {
            $("#matchEventServiceSpinner").hide();
            $("#runMatchEventService").show();
        },
        success: function(data) {
            $("#matchEventServiceSuccess").show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#matchEventServiceError").show();
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