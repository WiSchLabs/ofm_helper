function addParsingSettingItem(name, value, id) {
    var css_class = value ? "check" : "unchecked";
    $('#ParsingSettings').append(
        "<li id='" + id + "' class='parsing_setting_item'>" +
            "<span id='" + id + "' class='parsing_setting_check glyphicon glyphicon-" + css_class + "'></span>" +
            name +
        "</li>"
    );
}

$('document').ready( function (){

    $('#headingParserSettings').click(function(){
        if (! $('#collapseParserSettings').hasClass('in')) { // area is being opened
            $.get("/account/get_parsing_settings",
                function (data) {
                    $('#ParsingSettings').html('');
                    addParsingSettingItem("Mannschaft und Spielerstatistiken", data['parsing_player_statistics'] , 'parsing_player_statistics');
                    addParsingSettingItem("AWP Aufwertungsgrenzen", data['parsing_awp_boundaries'], 'parsing_awp_boundaries');
                    addParsingSettingItem("Finanzen", data['parsing_finances'], 'parsing_finances');
                    addParsingSettingItem("Alle Spiele", data['parsing_matches'], 'parsing_matches');
                    addParsingSettingItem("Ligaspiel-Details", data['parsing_match_details'], 'parsing_match_details');
                    addParsingSettingItem("Stadiondaten bei Heimspielen", data['parsing_stadium_details'], 'parsing_stadium_details');
                }
            );
        }
    });

    $('#ParsingSettings').on('click', '.parsing_setting_item', function() {
        var parsingSettingItem = $(this).find('.parsing_setting_check');
        var parsingSettingGotChecked = parsingSettingItem.hasClass("glyphicon-unchecked");
        var parsingSettingItemName = $(this).attr('id');
        var params = {};
        params[parsingSettingItemName] = parsingSettingGotChecked;
        $.post("/account/update_parsing_setting_item_status", params);

        if (parsingSettingGotChecked) {
            parsingSettingItem.removeClass('glyphicon-unchecked');
            parsingSettingItem.addClass('glyphicon-check');
        } else {
            parsingSettingItem.addClass('glyphicon-unchecked');
            parsingSettingItem.removeClass('glyphicon-check');
        }
    });

});
