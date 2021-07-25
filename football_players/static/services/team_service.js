$("#runTeamService").click(function() {
    $.ajax({
        url: "/api/team/",
        // shows the loader element before sending.
        beforeSend: function() {
            $("#runTeamService").hide();
            $("#teamServiceSpinner").show();
        },
        // hides the loader after completion of request, whether successfull or failor.
        complete: function() {
            $("#teamServiceSpinner").hide();
            $("#runTeamService").show();
        },
        success: function(data) {
            $("#teamServiceSuccess").show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#teamServiceError").show();
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