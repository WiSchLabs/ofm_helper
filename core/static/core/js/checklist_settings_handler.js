$('document').ready( function (){
    function addChecklistItem(item) {
        $('#checklist_items').append(
            "<div id='" + item['id'] + "' class='checklist_item_container new' style='opacity:0;'>" +
                "<span class='checklist_item_priority_handle glyphicon glyphicon-resize-vertical'></span>" +
                "<input type='text' class='form-control checklist_item_name' name='" + item['id'] + "_name' value='" + item['name'] + "'  maxlength='255'>" +
                "<span class='invisible checklist_item_saved alert-success glyphicon glyphicon-floppy-saved'></span>" +
                "<span class='delete_checklist_item alert-danger glyphicon glyphicon-trash'></span>" +
                "<div class='dropdown checklist_type'>" +
                    "<button class='btn btn-default dropdown-toggle' type='button' id='dropdownMenu1' data-toggle='dropdown' aria-haspopup='true' aria-expanded='true'>" +
                        "Wähle, wann dies angezeigt wird " +
                        "<span class='caret'></span>" +
                    "</button>" +
                    "<ul class='dropdown-menu'>" +
                        "<li class='everyday'><a href='#'>Jeden Spieltag (inkl. 0.)</a></li>" +
                        "<li class='home_match'><a href='#'>Wenn morgen Heimspiel ist</a></li>" +
                        "<li class='matchdays'><a href='#'>Bestimmte Spieltage</a></li>" +
                        "<li class='matchday_pattern'><a href='#'>Jeden X. Spieltag (exkl. 0.)</a></li>" +
                    "</ul>" +
                "</div>" +
                "<span class='current_type'></span>" +
                "<div class='checklist_item_matchdays hide' data-toggle='tooltip' title='Komma-getrennte List, z.B. 3,6,7'>" +
                    "<input class='form-control' type='text' name'" + item['id'] + "_matchdays' value='0' min='0' max='34' maxlength='255'> " +
                "</div>" +
                "<div class='input-group spinner checklist_item_matchday_pattern hide' data-toggle='tooltip' title='z.B. 5 heißt: 5, 10, 15, etc.'>" +
                    "<input class='form-control' type='number' name'" + item['id'] + "_matchday_pattern' value='1' min='1' max='17'>" +
                    "<div class='input-group-btn-vertical'>" +
                        "<button class='btn btn-default' type='button'><i class='glyphicon glyphicon-triangle-top'></i></button>" +
                        "<button class='btn btn-default' type='button'><i class='glyphicon glyphicon-triangle-bottom'></i></button>" +
                    "</div>" +
                "</div>" +
            "</div>"
        );
        var new_checklist_item = $('#checklist_items').find('.checklist_item_container').filter('.new');
        var item_types = new_checklist_item.find('.checklist_type li');
        var active_item_type = item_types.filter('.everyday');
        if (item['type_matchdays'] !== undefined) {
            active_item_type = item_types.filter('.matchdays');
            var matchday_input_container = new_checklist_item.find('.checklist_item_matchdays');
            matchday_input_container.find('input').val(item['type_matchdays']);
            matchday_input_container.removeClass('hide');
        }
        if (item['type_matchday_pattern'] !== undefined) {
            active_item_type = item_types.filter('.matchday_pattern');
            var matchday_pattern_input_container = new_checklist_item.find('.checklist_item_matchday_pattern');
            matchday_pattern_input_container.find('input').val(item['type_matchday_pattern']);
            matchday_pattern_input_container.removeClass('hide');
        }
        if (item['type_home_match']) { active_item_type = item_types.filter('.home_match'); }
        active_item_type.addClass('active');
        new_checklist_item.find('.current_type').html(active_item_type.find('a').html());
        new_checklist_item.animate({opacity:1}, 'fast');
        new_checklist_item.removeClass('new');

        new_checklist_item.find('[data-toggle="tooltip"]').tooltip();
        $( "#checklist_items" ).sortable();
    }

    $('#headingChecklistSettings').click(function(){
        if (! $('#collapseChecklistSettings').hasClass('in')) { // area is being opened
            $.get("/settings_get_checklist_items",
                function (data) {
                    $('#checklist_items').html('');
                    data.forEach(addChecklistItem);
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
            }
        );
    });

    $('#save_checklist_priority').click( function() {
        var params = {
            checklist_priority: $('#checklist_items').sortable("toArray").join(",")
        };
        $.post("/settings_update_checklist_priority", params);
        $('#checklist_items_priority_saved').removeClass('invisible');
        setTimeout(function() {
            $('#checklist_items_priority_saved').addClass('invisible');
        }, 2000);
    });

    function saveChecklistName(elem) {
        var params = {
            checklist_item_id: elem.closest('.checklist_item_container').attr('id'),
            checklist_item_name: elem.val()
        };
        $.post("/settings_update_checklist_item", params);
        elem.closest('.checklist_item_container').find('.checklist_item_saved').removeClass('invisible');
    }
    $('#checklist_items').on('focusout', '.checklist_item_name', function() {
        saveChecklistName($(this));
    });
    $('#checklist_items').on('keyup', '.checklist_item_name', function(event) {
        if (event.which == 13) {
            saveChecklistName($(this));
        }
    });
    $('#checklist_items').on('input', '.checklist_item_name', function() {
        $(this).closest('.checklist_item_container').find('.checklist_item_saved').addClass('invisible');
    });

    function saveChecklistMatchdays(elem) {
        var matchdays_input = elem.find('input');
        var matchday_min = matchdays_input.attr('min');
        var matchday_max = matchdays_input.attr('max');
        var matchdays = new Set();
        matchdays_input.val().split(",").forEach(function(matchday_val, index, array){
            var matchday = matchday_min;
            if($.isNumeric(matchday_val)) { matchday = +matchday_val; }
            if (matchday < matchday_min) { matchday = matchday_min; }
            if (matchday > matchday_max) { matchday = matchday_max; }
            matchdays.add(matchday);
        });
        var sorted_matchdays = Array.from(matchdays).sort(function(a, b){return a-b});
        var comma_separated_matchdays = sorted_matchdays.join(",");
        matchdays_input.val(comma_separated_matchdays);
        var params = {
            checklist_item_id: elem.closest('.checklist_item_container').attr('id'),
            checklist_item_matchdays: comma_separated_matchdays
        };
        $.post("/settings_update_checklist_item", params);
        elem.closest('.checklist_item_container').find('.checklist_item_saved').removeClass('invisible');
    }
    $('#checklist_items').on('focusout', '.checklist_item_matchdays', function() {
        saveChecklistMatchdays($(this));
    });
    $('#checklist_items').on('click', '.checklist_item_matchdays button', function() {
        saveChecklistMatchdays($(this));
    });
    $('#checklist_items').on('keyup', '.checklist_item_matchdays', function(event) {
        if (event.which == 13) {
            saveChecklistMatchdays($(this));
        }
    });
    $('#checklist_items').on('input', '.checklist_item_matchdays', function() {
        $(this).closest('.checklist_item_container').find('.checklist_item_saved').addClass('invisible');
    });

    function saveChecklistMatchdayPattern(elem) {
        var matchday_pattern_input = elem.find('input');
        var matchday_pattern_min = matchday_pattern_input.attr('min');
        var matchday_pattern_max = matchday_pattern_input.attr('max');
        var matchday_pattern = matchday_pattern_min;
        if($.isNumeric(matchday_pattern_input.val())) { matchday_pattern = +matchday_pattern_input.val(); }
        if (matchday_pattern < matchday_pattern_min) { matchday_pattern = matchday_pattern_min; }
        if (matchday_pattern > matchday_pattern_max) { matchday_pattern = matchday_pattern_max; }
        matchday_pattern_input.val(matchday_pattern);
        var params = {
            checklist_item_id: elem.closest('.checklist_item_container').attr('id'),
            checklist_item_matchday_pattern: matchday_pattern
        };
        $.post("/settings_update_checklist_item", params);
        elem.closest('.checklist_item_container').find('.checklist_item_saved').removeClass('invisible');
    }
    $('#checklist_items').on('focusout', '.checklist_item_matchday_pattern', function() {
        saveChecklistMatchdayPattern($(this));
    });
    $('#checklist_items').on('click', '.checklist_item_matchday_pattern button', function() {
        saveChecklistMatchdayPattern($(this));
    });
    $('#checklist_items').on('keyup', '.checklist_item_matchday_pattern', function(event) {
        if (event.which == 13) {
            saveChecklistMatchdayPattern($(this));
        }
    });
    $('#checklist_items').on('input', '.checklist_item_matchday_pattern', function() {
        $(this).closest('.checklist_item_container').find('.checklist_item_saved').addClass('invisible');
    });

    $('#checklist_items').on('click', '.delete_checklist_item', function() {
        var checklist_item = $(this).closest('.checklist_item_container');
        var params = {
            checklist_item_id: checklist_item.attr('id')
        };
        $.post("/settings_delete_checklist_item", params);
        checklist_item.animate({opacity:0, height:0}, 200);
        setTimeout(function() {
            checklist_item.remove();
        }, 200);
    });

    $('#checklist_items').on('click', '.checklist_type a', function(event) {
        event.stopPropagation();
        event.preventDefault();

        var checklist_item = $(this).closest('.checklist_item_container');
        checklist_item.find('.checklist_type li').removeClass('active');
        $(this).parent('li').addClass('active');
        var checklist_item_type = checklist_item.find('li').filter('.active');
        checklist_item.find('.current_type').html($(this).html());

        var matchdays_input = checklist_item.find('.checklist_item_matchdays');
        var matchday_pattern_input = checklist_item.find('.checklist_item_matchday_pattern');
        matchdays_input.addClass('hide');
        matchday_pattern_input.addClass('hide');

        var params = {
            checklist_item_id: checklist_item.attr('id')
        };
        if (checklist_item_type.hasClass('matchdays')) {
            matchdays_input.removeClass('hide');
            params['checklist_item_matchdays'] = matchdays_input.find('input').val();
        }
        else if (checklist_item_type.hasClass('matchday_pattern')) {
            matchday_pattern_input.removeClass('hide');
            params['checklist_item_matchday_pattern'] = matchday_pattern_input.find('input').val();
        }
        else if (checklist_item_type.hasClass('home_match')) {
            params['checklist_item_home_match'] = true;
        }
        else {
            params['checklist_item_everyday'] = true;
        }

        $.post("/settings_update_checklist_item", params);
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
