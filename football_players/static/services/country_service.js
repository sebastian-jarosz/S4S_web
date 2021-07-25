$("#runCountryService").click(function() {
    $.ajax({
        url: "/api/country/",
        // shows the loader element before sending.
        beforeSend: function() {
            $("#runCountryService").hide();
            $("#countryServiceSpinner").show();
        },
        // hides the loader after completion of request, whether successfull or failor.
        complete: function() {
            $("#countryServiceSpinner").hide();
            $("#runCountryService").show();
        },
        success: function(data) {
            $("#countryServiceSuccess").show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#countryServiceError").show();
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