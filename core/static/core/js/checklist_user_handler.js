function showChecklistItem(item) {
    $('#Checklist').append(
        "<li id='" + item['id'] + "' class='checklist_entry checkbox new'>" +
            "<span class='checklist_check glyphicon glyphicon-unchecked' id='" + item['id'] + "_check'></span>" +
            item['name'] +
        "</li>"
    );
    var new_checklist_entry =  $('#Checklist').find('.checklist_entry').filter('.new');
    if (item['checked']) {
       new_checklist_entry.find('.checklist_check').removeClass('glyphicon-unchecked');
       new_checklist_entry.find('.checklist_check').addClass('glyphicon-check');
    }
    new_checklist_entry.removeClass('new');
}

$('document').ready( function (){
    $(function() {
        $('#ChecklistContainer').append(
            "<div class='btn-group'>" +
                "<button type='button' class='btn btn-default dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
                    "<span class='glyphicon glyphicon-list'></span> Checkliste <span class='caret'></span>" +
                "</button>" +
                "<ul id='Checklist' class='dropdown-menu dropdown-menu-right'></ul>" +
            "</div>"
        );
        $.get("/settings_get_checklist_items_for_today",
            function (data) {
                $('#Checklist').html('');
                data.forEach(showChecklistItem);
            }
        );
    });

    $('#ChecklistContainer').on('click', '.checklist_entry', function() {
        var checklistItem = $(this).find('.checklist_check');
        var checklistItemGotChecked = checklistItem.hasClass("glyphicon-unchecked");
        var params = {
            checklist_item_id: $(this).attr('id'),
            checklist_item_checked: checklistItemGotChecked
        };
        $.post("/settings_update_checklist_item", params);
        $('#ChecklistContainer').find('.btn-group').addClass('open');
        if (checklistItemGotChecked) {
            checklistItem.removeClass('glyphicon-unchecked');
            checklistItem.addClass('glyphicon-check');
        } else {
            checklistItem.addClass('glyphicon-unchecked');
            checklistItem.removeClass('glyphicon-check');
        }
    });
});
