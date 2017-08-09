/**
 * Created by Administrator on 2017/8/1 0001.
 */
$(function() {
    "use strict";

    var data = [],
        totalPoints = 300;

    if ($('#flot_bar_chart').length > 0) {
        ini_bartchart(0, '#flot_bar_chart', '#fcb03b', 10);
    }

    if ($('#flot_bar_chart_1').length > 0) {
        ini_bartchart(1, '#flot_bar_chart_1', 'red', 10);
    }
});

function ini_bartchart(index_data, id_name, bar_corler, total_length){
     /*Defining Option*/
        var barOptions = {
            series: {
                bars: {
                    show: true,
                    barWidth: 40000000
                }
            },
            yaxis: {
                min:0,
                minTickSize: [1],
                font: {
                    color: '#2f2c2c'
                }
            },
            xaxis: {
                mode: "time",
                timeformat: "%m-%d",
                minTickSize: [1, "day"],
                font: {
                    color: '#2f2c2c'
                }
            },

            legend: {
                show: false
            },
            grid: {
                color: "#eee",
                hoverable: true,
                borderWidth: 0,
                backgroundColor: '#FFF'
            },
            tooltip: true,
            tooltipOpts: {
                content: "%x，销售: %y 件",
                defaultTheme: false
            }
        };

        /*Defining Data*/
        var data_list = [];
        for (var i = 0; i < total_length; i++) {
            var start = -20000000+delta_date*86400000;
            var data_temp = [start + i * 86400000, sale_list[index_data][9-i]];
            data_list.push(data_temp);
        }
        var barData = {
            label: "bar",
            color: bar_corler,
            data: data_list
        };

        /*Plot*/
        $.plot($(id_name), [barData], barOptions);
}