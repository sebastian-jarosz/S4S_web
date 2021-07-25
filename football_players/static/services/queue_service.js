$("#runQueueService").click(function() {
    $.ajax({
        url: "/api/queue/",
        // shows the loader element before sending.
        beforeSend: function() {
            $("#runQueueService").hide();
            $("#queueServiceSpinner").show();
        },
        // hides the loader after completion of request, whether successfull or failor.
        complete: function() {
            $("#queueServiceSpinner").hide();
            $("#runQueueService").show();
        },
        success: function(data) {
            $("#queueServiceSuccess").show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#queueServiceError").show();
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