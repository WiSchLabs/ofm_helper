var $tables = $('.statistics_table');
var selected_config = "";

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

$("#strength-slider-label").html('Gemittelte Stärke');
$("#strength-slider-label").attr('title', "Harmonisches Mittel beider eingegebenen Mannschaftsstärken");
$("#strength-slider").slider({labelledby: 'strength-slider-label'});

$("#tolerance-slider-label").attr('title', "Toleranzwert um die gemittelte Stärke");


function get_current_params(){
    var strength1 = parseInt($('#strength-slider').attr('value').split(',')[0], 10);
    var strength2 = parseInt($('#strength-slider').attr('value').split(',')[1], 10);
    var tolerance = parseInt($('#tolerance-slider').attr('value'), 10);

    set_cookie('slider_min', strength1, 1);
    set_cookie('slider_max', strength2, 1);
    set_cookie('tolerance', tolerance, 1);

    var params = {
        tolerance: $('#tolerance-slider').attr('value'),
        harmonic_strength: Number(2*strength1*strength2/(strength1+strength2)).toFixed(0),
        configuration_filter: selected_config
    };

    return params;
}

function set_cookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        expires = "; expires="+date.toGMTString();
    }
    document.cookie = name+"="+value+expires+"; path=/";
}

function update_stadium_statistics() {
    var params = get_current_params();

    $.get(JSON_URL, params, function (returnedData) {
            $tables.bootstrapTable('removeAll');
            $tables.bootstrapTable('load', returnedData);
        }
    );
}

$('#strength-slider').slider().on('slideStop', function(event){
    update_stadium_statistics();
});

$('#tolerance-slider').slider().on('slideStop', function(event){
    update_stadium_statistics();
});


$("#StadiumConfigFilter a").click(function(){
    $("#StadiumConfigFilter a").removeClass('selected');
    $(this).addClass('selected');

    /** only show clear filter button, if a filter is set */
    var clear_filter = $("#StadiumConfigFilter .clear_filter");
    if (clear_filter.find('a').hasClass('selected')) {
        clear_filter.addClass('hide');
    } else {
        clear_filter.removeClass('hide');
    }

    selected_config = $(this).attr('data-value');
    update_stadium_statistics();
});

$(document).ready(function() {
    update_stadium_statistics;
});