function table_loader() {
    var $tables = $('.statistics_table'),
        newer_matchday, newer_matchday_season,
        older_matchday, older_matchday_season,
        season;

    function updateData(event, data) {
        var params = {};

        if (data) {
            params = {
                newer_matchday_season: newer_matchday_season, newer_matchday: newer_matchday,
                older_matchday_season: older_matchday_season, older_matchday: older_matchday
            };
        } else {
            params = {newer_matchday_season: newer_matchday_season, newer_matchday: newer_matchday};
        }
        $.get(JSON_URL, params,
            function (returnedData) {
                $tables.bootstrapTable('removeAll');
                $tables.bootstrapTable('load', returnedData);

                if (data) {
                    $('#matchday_compare').removeClass('hide')
                } else {
                    $('#matchday_compare').addClass('hide')
                }

                markSpecialValues();
            }
        );
    }

    $('#season').on('change', function () {
        season = $("#season").val();
        $.get(JSON_URL, {season: season},
            function (returnedData) {
                $tables.bootstrapTable('removeAll');
                $tables.bootstrapTable('load', returnedData);
            }
        );
    });

    $('#newer_matchday').on('change', function () {
        newer_matchday_season = $("#newer_matchday").val().split("/")[0];
        newer_matchday = $("#newer_matchday").val().split("/")[1];
        updateData(event, $('#diff_toggle').prop('checked'));
    });
    $('#older_matchday').on('change', function () {
        newer_matchday_season = $("#newer_matchday").val().split("/")[0];
        newer_matchday = $("#newer_matchday").val().split("/")[1];
        older_matchday_season = $("#older_matchday").val().split("/")[0];
        older_matchday = $("#older_matchday").val().split("/")[1];
        updateData(event, $('#diff_toggle').prop('checked'));
    });


    $('#diff_toggle').bootstrapSwitch('state', false);

    $('#diff_toggle').on('switchChange.bootstrapSwitch', function (event, data) {
        newer_matchday_season = $("#newer_matchday").val().split("/")[0];
        newer_matchday = $("#newer_matchday").val().split("/")[1];
        older_matchday_season = $("#older_matchday").val().split("/")[0];
        older_matchday = $("#older_matchday").val().split("/")[1];
        var params = {};

        if (data) {
            params = {
                newer_matchday_season: newer_matchday_season, newer_matchday: newer_matchday,
                older_matchday_season: older_matchday_season, older_matchday: older_matchday
            };
        } else {
            params = {newer_matchday_season: newer_matchday_season, newer_matchday: newer_matchday};
        }

        $.get(JSON_URL, params,
            function (returnedData) {
                $tables.bootstrapTable('removeAll');
                $tables.bootstrapTable('load', returnedData);

                if (data) {
                    $('#matchday_compare').removeClass('hide')
                } else {
                    $('#matchday_compare').addClass('hide')
                }

                markSpecialValues();
            }
        );
    });

    function markSpecialValues() {
        $('.statistics_table .statistic_mark').each(function () {
            if ($(this).hasClass('statistic_mark_gain')) {
                $(this).parent().addClass("bg-success");
            } else if ($(this).hasClass('statistic_mark_lost')) {
                $(this).parent().addClass("bg-danger");
            } else {
                $(this).parent().removeClass("bg-success");
                $(this).parent().removeClass("bg-danger");
            }
        })
    }

    function queryParams() {
        var params = {};
        $('#table-toolbar').find('input[name]').each(function () {
            params[$(this).attr('name')] = $(this).val();
        });
        return params;
    }
}

function moneyDiffFormatter(value) {
    var is_diff = $('#diff_toggle').bootstrapSwitch('state');

    var color = 'statistic_mark ';
    if (is_diff) {
        if (value > 0) {
            color += "statistic_mark_gain";
        } else if (value < 0) {
            color += "statistic_mark_lost";
        }
    }

    return '<span class="' + color + '">' + moneyFormatter(value) + '</span>';
}

function numberDiffFormatter(value) {
    var is_diff = $('#diff_toggle').bootstrapSwitch('state');

    var color = 'statistic_mark ';
    if (is_diff) {
        if (value > 0) {
            color += "statistic_mark_gain";
        } else if (value < 0) {
            color += "statistic_mark_lost";
        }
    }

    return '<span class="' + color + '">' + numberFormatter(value) + '</span>';
}

function numberFormatter(value) {
    return value.toLocaleString('de');
}
function moneyFormatter(value) {
    return numberFormatter(value) + " &euro;";
}

window.onload=table_loader;