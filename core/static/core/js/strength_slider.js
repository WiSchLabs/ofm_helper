var $tables = $('.statistics_table')

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});

$("#strength-slider-label").html('Gemittelte Stärke');
$("#strength-slider-label").attr('title', "Harmonisches Mittel beider eingegebenen Mannschaftsstärken");
$("#strength-slider").slider({labelledby: 'strength-slider-label'});

$("#tolerance-slider-label").attr('title', "Toleranzwert um die gemittelte Stärke");


function get_current_params(){
    var strength1 = parseInt($('#strength-slider').attr('value').split(',')[0], 10);
    var strength2 = parseInt($('#strength-slider').attr('value').split(',')[1], 10);

    set_cookie('slider_min', strength1, 1);
    set_cookie('slider_max', strength2, 1);

    var params = {
        tolerance: $('#tolerance-slider').attr('value'),
        harmonic_strength: Number(2*strength1*strength2/(strength1+strength2)).toFixed(0)
    };

    return params;
}

function set_cookie(name, value, days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else var expires = "";
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
    update_stadium_statistics()
});

$('#tolerance-slider').slider().on('slideStop', function(event){
    update_stadium_statistics()
});

$(document).ready(function() {
    update_stadium_statistics;
});