$("#runLeagueService").click(function() {
    $.ajax({
        url: "/api/league/",
        // shows the loader element before sending.
        beforeSend: function() {
            $("#runLeagueService").hide();
            $("#leagueServiceSpinner").show();
        },
        // hides the loader after completion of request, whether successfull or failor.
        complete: function() {
            $("#leagueServiceSpinner").hide();
            $("#runLeagueService").show();
        },
        success: function(data) {
            $("#leagueServiceSuccess").show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#leagueServiceError").show();
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