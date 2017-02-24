var transfers_chart_options =  {
    chart: {
        type: 'boxplot',
        height: 650,
        zoomType: 'xy',
        panKey: 'ctrl',
        panning: true
    },
    title: {
        text: 'Spielerpreise'
    },
    xAxis: {
        categories: [], // has to be overwritten
        title: {
            text: 'Stärke'
        }
    },
    yAxis: {
        title: {
            text: 'Preis'
        }
    },
    plotOptions: {
        boxplot: {
            fillColor: '#F0F0E0',
            lineWidth: 1.5,
            medianColor: '#24a52f',
            medianWidth: 2,
            stemWidth: 2,
            whiskerColor: '#24a52f',
            whiskerLength: '40%'
        }
    },
    series: [] // has to be overwritten
};

var detail_groupby = 'Strength';
var overview_groupby = 'Strength,Age';
var strengths = '';
var positions = '';
var ages = '';
var seasons = '';
var matchdays = '';

function resetFilterValues(){
    detail_groupby = 'Strength';
    overview_groupby = 'Strength,Age';
    strengths = '';
    positions = '';
    ages = '';
    seasons = '';
    matchdays = '';
    $('.selectpicker').val('');
    $('#TransferGroupByFilter').find("option[value='Strength']").prop('selected', true);
    $('#TransferOverviewGroupByFilter').find("option[value='Strength'], option[value='Age']").prop('selected', true);
    $('.selectpicker').selectpicker('refresh');
}

function requestChartDetailData() {
    $.ajax({
        type: "GET",
        url: transfersDetailChartJsonURL,
        data: {
            group_by: detail_groupby,
            positions: positions,
            strengths: strengths,
            ages: ages,
            seasons: seasons,
            matchdays: matchdays
        },
        dataType: 'json',
        success: function (data) {
            transfers_chart_options.series = data['series'];
            transfers_chart_options.xAxis.categories = data['categories'];
            transfers_chart_options.xAxis.title.text=translateGroupby();
            $('#transfers_chart_container').highcharts(transfers_chart_options);

            var filters = ['ages', 'strengths', 'positions', 'seasons', 'matchdays'];

            filters.forEach(function(filter) {
                var filter_id = 'Transfer' + filter[0].toUpperCase() + filter.substring(1) + 'Filter';
                fillFilterDropdown(filter_id, data[filter])
            });
            $('.selectpicker').selectpicker('refresh');
        }
    });
}

function translateGroupby(){
    var translation = '';
    if (detail_groupby === 'Strength'){
        translation = 'Stärke';
    }
    if (detail_groupby === 'Age'){
        translation = 'Alter';
    }
    if (detail_groupby === 'Position'){
        translation = 'Position';
    }
    if (detail_groupby === 'Season'){
        translation = 'Saison';
    }
    if (detail_groupby === 'Matchday'){
        translation = 'Spieltag';
    }
    return translation;
}

function fillFilterDropdown(filter_id, attribute) {
    var filter = $('#' + filter_id);
    if ($.trim(filter.html()) === '') {
        attribute.forEach(function (item) {
            $('#' + filter_id).append("<option value='" + item + "'>" + item + "</option>");
        });
    }
}

function initFilters(){
    $('.selectpicker').selectpicker({
        actionsBox: true,
        selectAllText: 'Alle',
        deselectAllText: 'Keiner',
        noneSelectedText: 'Alle',
        showTick: true,
        width: '100%'
    });

    $('#TransferOverviewGroupByFilter').selectpicker({
        noneSelectedText: 'Keine Gruppierung gewählt',
        maxOptions: 2
    });
}

function addFilterOnChangeHandlers(){
    $('#TransferGroupByFilter').change(function () {
        detail_groupby = $(this).val();
    });

    $('#TransferOverviewGroupByFilter').change(function () {
        overview_groupby = getFilterValues($(this));
    });

    $('#TransferPositionsFilter').change(function () {
        positions = getFilterValues($(this));
    });

    $('#TransferAgesFilter').change(function () {
        ages = getFilterValues($(this));
    });

    $('#TransferStrengthsFilter').change(function () {
        strengths = getFilterValues($(this));
    });

    $('#TransferSeasonsFilter').change(function () {
        seasons = getFilterValues($(this));
    });

    $('#TransferMatchdaysFilter').change(function () {
        matchdays = getFilterValues($(this));
    });

    function getFilterValues(filter) {
        if (filter.val()) {
            return filter.val().join(",");
        } else {
            return ''
        }
    }
}

function addButtonClickHandlers() {
    $('.TransferFilterApplyButton').click(function(){
        requestChartDetailData();
        requestOverviewTableData();
        setTimeout(makeTableSelectable, 1000);
    });

    $('.TransferResetButton').click(function(){
        resetFilterValues();
        requestChartDetailData();
        requestOverviewTableData();
        setTimeout(makeTableSelectable, 1000);
    });
}

function requestOverviewTableData() {
    $.ajax({
        type: "GET",
        url: transfersOverviewTableJsonURL,
        data: {
            group_by: overview_groupby,
            positions: positions,
            strengths: strengths,
            ages: ages,
            seasons: seasons,
            matchdays: matchdays
        },
        dataType: 'json',
        success: function (data) {
            fillOverviewTable(data);
        }
    });
}

function fillOverviewTable(data){
    $('#TransfersOverviewTable').html('');

    var header_row = '<tr><th></th>';

    var group1Length = data.group1.length;
    for (var k = 0; k < group1Length; k++) {
        header_row += '<th>' + data.group1[k] + '</th>'
    }
    header_row += '</tr>';

    $('#TransfersOverviewTable').append(header_row);

    var group2Length = data.group2.length;
    for (var i = 0; i < group2Length; i++) {
        var row = '<tr><th>' + data.group2[i] + '</th>';

        var rowLength = data.medians[i].length;
        for (var j = 0; j < rowLength; j++) {
            row += '<td>' + data.medians[i][j] + '</td>';
        }

        row += '</tr>';
        $('#TransfersOverviewTable').append(row);
    }
}

function makeTableSelectable(){
    var cells = $('td');

    cells.on('click', function (e) {
        var cell = $(this);

        if (!(e.ctrlKey || e.metaKey)) {
            /* If CTRL key pressed, highlight the other cell that was clicked */
            /* Otherwise just highlight one cell and clean other cells */
            cells.removeClass('success');
        }
        if (cell.hasClass('success')) {
            cell.removeClass('success');
        } else {
            cell.addClass('success');
        }
    });
}

$(function () {
    initFilters();

    addFilterOnChangeHandlers();
    addButtonClickHandlers();

    requestChartDetailData();
    requestOverviewTableData();

    setTimeout(makeTableSelectable, 1000);
});
