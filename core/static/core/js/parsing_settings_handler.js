function addParsingSettingItem(name, value, id) {
    $('#ParsingSettings').append(
        "<li id='" + id + "' class='parsing_setting_item'>" +
            "<span class='parsing_setting_check glyphicon glyphicon-unchecked'></span>" +
            name +
        "</li>"
    );
    var new_item = findCheckboxByItemId(id);
    if (value) { checkItem(new_item); }
}

function findCheckboxByItemId(id) {
    return $('#'+id).find('.parsing_setting_check');
}

function checkItem(item) {
    item.addClass('glyphicon-check');
    item.removeClass('glyphicon-unchecked');
}

function uncheckItem(item) {
    item.removeClass('glyphicon-check');
    item.addClass('glyphicon-unchecked');
}

function disableItem(item) {
    uncheckItem(item);
    item.parent('li').addClass('disabled');
}

function enableItem(item) {
    item.parent('li').removeClass('disabled');
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


                    findCheckboxByItemId('parsing_match_details').addClass('subitem');
                    findCheckboxByItemId('parsing_stadium_details').addClass('sub-subitem');

                    if (!data['parsing_matches']) {
                        disableItem(findCheckboxByItemId('parsing_match_details'));
                    }
                    if (!data['parsing_match_details']) {
                        disableItem(findCheckboxByItemId('parsing_stadium_details'));
                    }
                }
            );
        }
    });

    $('#ParsingSettings').on('click', '.parsing_setting_item', function() {
        if ($(this).hasClass("disabled")) {
            return
        }
        var parsingSettingItem = $(this).find('.parsing_setting_check');
        var parsingSettingGotChecked = parsingSettingItem.hasClass("glyphicon-unchecked");
        var parsingSettingItemName = $(this).attr('id');
        var params = {};
        params[parsingSettingItemName] = parsingSettingGotChecked;
        $.post("/account/update_parsing_setting_item_status", params);

        if (parsingSettingGotChecked) {
            checkItem(parsingSettingItem);
        } else {
            uncheckItem(parsingSettingItem);
        }

        if ($(this).attr('id') == "parsing_matches" && parsingSettingGotChecked) {
            enableItem(findCheckboxByItemId('parsing_match_details'));
        } else if ($(this).attr('id') == "parsing_matches" && !parsingSettingGotChecked) {
            disableItem(findCheckboxByItemId('parsing_match_details'));
            disableItem(findCheckboxByItemId('parsing_stadium_details'));
        }

        if ($(this).attr('id') == "parsing_match_details" && parsingSettingGotChecked) {
            enableItem(findCheckboxByItemId('parsing_stadium_details'));
        } else if ($(this).attr('id') == "parsing_match_details" && !parsingSettingGotChecked) {
            disableItem(findCheckboxByItemId('parsing_stadium_details'));
        }

    });

});
