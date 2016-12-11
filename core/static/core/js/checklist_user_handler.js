function showChecklistItem(item) {
    $('#ChecklistSubMenu').append(
        "<li id='" + item['id'] + "' class='checklist_entry new'>" +
            "<span class='checklist_check glyphicon glyphicon-unchecked' id='" + item['id'] + "_check'></span>" +
            item['name'] +
        "</li>"
    );
    var new_checklist_entry =  $('#ChecklistSubMenu').find('.checklist_entry').filter('.new');
    if (item['checked']) {
       new_checklist_entry.find('.checklist_check').removeClass('glyphicon-unchecked');
       new_checklist_entry.find('.checklist_check').addClass('glyphicon-check');
    }
    new_checklist_entry.removeClass('new');
}

$('document').ready( function (){
    $(function() {
        $.get("/checklist/get_checklist_items_for_today",
            function (data) {
                $('#ChecklistSubMenu').html('');
                data.forEach(showChecklistItem);
            }
        );
        $.get("/ofm/get_current_matchday",
            function (data) {
                $('#ChecklistBar').find('a').append(
                    "<span class='current_matchday'>" +
                        "<span class='glyphicon glyphicon-calendar'></span> " +
                        data['matchday_number'] +
                        "/" +
                        data['season_number'] +
                    "</span>"
                );
            }
        );
        var checklist_open = get_cookie("checklist_open");
        if (checklist_open == 'true') {
            setTimeout(function() {
                $('#ChecklistSubMenu').collapse('show');
            }, 1000); // wait for data to be loaded
        }
    });

    $('#ChecklistBar').on('click', function() {
        set_cookie('checklist_open', !$('#ChecklistSubMenu').hasClass('in'), 1);
    });

    $('#ChecklistSubMenu').on('click', '.checklist_entry', function() {
        var checklistItem = $(this).find('.checklist_check');
        var checklistItemGotChecked = checklistItem.hasClass("glyphicon-unchecked");
        var params = {
            checklist_item_id: $(this).attr('id'),
            checklist_item_checked: checklistItemGotChecked
        };
        $.post("/checklist/update_checklist_item", params);

        if (checklistItemGotChecked) {
            checklistItem.removeClass('glyphicon-unchecked');
            checklistItem.addClass('glyphicon-check');
        } else {
            checklistItem.addClass('glyphicon-unchecked');
            checklistItem.removeClass('glyphicon-check');
        }
    });
});
