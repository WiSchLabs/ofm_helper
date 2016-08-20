var chart_options = {
    chart: {
        type: 'spline' // default; can be overwritten
    },
    title: {
        text: 'Statistik'
    },
    xAxis: {
        title: {
            text: 'Spieltag'
        },
        categories: [] // has to be overwritten
    },
    yAxis: {
        title: {
            text: ' '
        }
    },
    plotOptions: {
        column: { // only relevant for chart.type = column
            stacking: 'normal'
        }
    },
    series: [] // has to be overwritten
};

$(function () {
    requestChartData(season_number);
});