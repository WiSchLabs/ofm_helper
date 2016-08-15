function finances_table_loader() {
    var $tables = $('.finances_table'),
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

        $.get(FINANCES_JSON_URL, params,
            function (returnedData) {
                $tables.bootstrapTable('removeAll');
                $tables.bootstrapTable('load', returnedData);

                if (data) {
                    $('#matchday_compare').removeClass('hide')
                } else {
                    $('#matchday_compare').addClass('hide')
                }

                markSpecialValues(data);
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

        $.get(FINANCES_JSON_URL, params,
            function (returnedData) {
                $tables.bootstrapTable('removeAll');
                $tables.bootstrapTable('load', returnedData);

                if (data) {
                    $('#matchday_compare').removeClass('hide')
                } else {
                    $('#matchday_compare').addClass('hide')
                }

                markSpecialValues(data);
            }
        );
    });

    function markSpecialValues(showing_diff) {
        $('.finances_table tr').each(function () {
            $(this).find('td').each(function () {
                var entry_value = $(this).html();
                $(this).html(Number(entry_value).toLocaleString('de'));

                if (showing_diff) {
                    if (entry_value > 0) {
                        $(this).addClass("bg-success");
                    } else if (entry_value < 0) {
                        $(this).addClass("bg-danger");
                    }
                } else {
                    $(this).removeClass("bg-success");
                    $(this).removeClass("bg-danger");
                }
            })
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

window.onload=finances_table_loader;