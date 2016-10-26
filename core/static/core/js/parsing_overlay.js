$("form.parseTrigger").append("<button type='submit' class='btn btn-default' id='OfmParseTrigger'><span class='glyphicon glyphicon-refresh'></span> jetzt diese Kategorie parsen</button>");
$('#OfmParseTrigger').click(function() {
    $("body").append("<div class='overlay'><div id='loading-img'><span>Die Daten werden geladen. Bitte Geduld.</span></div></div>");
    $(".overlay").show();
});