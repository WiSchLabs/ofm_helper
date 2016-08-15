function table_loader() {
    var $tables = $('.statistics_table'),
        newer_matchday, newer_matchday_season,
        older_matchday, older_matchday_season;

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
            }
        );
    }

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
            }
        );
    });

    function queryParams() {
        var params = {};
        $('#table-toolbar').find('input[name]').each(function () {
            params[$(this).attr('name')] = $(this).val();
        });
        return params;
    }
}

function balanceFormatter(value) {
    var color = '';
    if (value > 0) {
        color = COLOR_SUCCESS;
    } else if(value < 0) {
        color = COLOR_DANGER;
    }

    return '<div style="color: ' + color + '">' + numberFormatter(value) + '</div>';
}

function numberFormatter(value) {
    return value.toLocaleString('de');
}

window.onload=table_loader;