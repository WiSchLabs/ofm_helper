$('document').ready( function (){
    function addChecklistItem(item) {
        $('#checklist_items').append(
            "<div id='" + item['id'] + "' style='opacity:0;'>" +
                "<input type='text' class='form-control checklist_item' name='" + item['id'] + "_name' value='" + item['name'] + "'  maxlength='255'>" +
                "<span class='delete_checklist_item alert-danger glyphicon glyphicon-trash'></span>" +
                "<div class='dropdown'>" +
                    "<button class='btn btn-default dropdown-toggle' type='button' id='dropdownMenu1' data-toggle='dropdown' aria-haspopup='true' aria-expanded='true'>" +
                        "Wähle aus, wann dies angezeigt werden soll " +
                        "<span class='caret'></span>" +
                    "</button>" +
                    "<ul class='dropdown-menu'>" +
                        "<li class='active'><a href='#'>Jeden Tag</a></li>" +
                        "<li><a href='#'>Morgen ist Heimspiel</a></li>" +
                        "<li><a href='#'>An einem bestimmten Spieltag</a></li>" +
                        "<li><a href='#'>Jeden X. Spieltag</a></li>" +
                    "</ul>" +
                "</div>" +
                "<div class='input-group spinner hide'>" +
                    "<input class='form-control' type'number' name'" + item['id'] + "_matchday' value='0' min='0' max='34'> " +
                    "<div class='input-group-btn-vertical'>" +
                        "<button class='btn btn-default' type='button'><i class='glyphicon glyphicon-triangle-top'></i></button>" +
                        "<button class='btn btn-default' type='button'><i class='glyphicon glyphicon-triangle-bottom'></i></button>" +
                    "</div>" +
                "</div>" +
                "<div class='input-group spinner hide'>" +
                    "<input class='form-control' type'number' name'" + item['id'] + "_matchday_pattern' value='1' min='1' max='17'>" +
                    "<div class='input-group-btn-vertical'>" +
                        "<button class='btn btn-default' type='button'><i class='glyphicon glyphicon-triangle-top'></i></button>" +
                        "<button class='btn btn-default' type='button'><i class='glyphicon glyphicon-triangle-bottom'></i></button>" +
                    "</div>" +
                "</div>" +
            "</div>"
        );
        $('#checklist_items').find('.checklist_item').parent('div').animate({opacity:1}, 'fast');
    }

    $('#headingChecklistSettings').click(function(){
        if (! $('#collapseChecklistSettings').hasClass('in')) { // area is being opened
            $.get("/settings_get_checklist_items",
                function (data) {
                    $('#checklist_items').html('');
                    data.forEach(addChecklistItem);
                    if(data.length != 0) {
                        $('#collapseChecklistSettings').find('span').html('');
                    }
                }
            );
        }
    });

    $('#add_checklist_item').click( function(event) {
        event.stopPropagation();
        event.preventDefault();
        $.get("/settings_add_checklist_item",
            function (data) {
                addChecklistItem(data);
                $('#collapseChecklistSettings').find('span').html('');
            }
        );
    });

    $('#checklist_items').on('focusout', '.checklist_item', function() {
        var params = {
            checklist_item_id: $(this).parent('div').attr('id'),
            checklist_item_name: $(this).val()
        };
        $.post("/settings_update_checklist_item", params);
    });

    $('#checklist_items').on('click', '.delete_checklist_item', function() {
        var checklist_item = $(this).parent('div');
        var params = {
            checklist_item_id: checklist_item.attr('id')
        };
        $.post("/settings_delete_checklist_item", params);
        checklist_item.animate({opacity:0, height:0}, 200);
        setTimeout(function() {
            checklist_item.remove();
        }, 200);
    });


    $(function(){
        $('#checklist_items').on('click', '.spinner .btn:first-of-type', function() {
          var btn = $(this);
          var input = btn.closest('.spinner').find('input');
          if (input.attr('max') == undefined || parseInt(input.val()) < parseInt(input.attr('max'))) {
            input.val(parseInt(input.val(), 10) + 1);
          } else {
            btn.next("disabled", true);
          }
        });
        $('#checklist_items').on('click', '.spinner .btn:last-of-type', function() {
          var btn = $(this);
          var input = btn.closest('.spinner').find('input');
          if (input.attr('min') == undefined || parseInt(input.val()) > parseInt(input.attr('min'))) {
            input.val(parseInt(input.val(), 10) - 1);
          } else {
            btn.prev("disabled", true);
          }
        });
    })

})
