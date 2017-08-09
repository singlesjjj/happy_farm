/**
 * Created by Administrator on 2017/8/1 0001.
 */
/*Dashboard Init*/

"use strict";

/*****Ready function start*****/
$(document).ready(function(){
	$('#statement').DataTable({
		"bFilter": false,
		"bLengthChange": false,
		"bPaginate": false,
		"bInfo": false
	});
	var dd_af = get_xaxis_date(date_list);
	if( $('#chart_1').length > 0 ){
		var ctx1 = document.getElementById("chart_1").getContext("2d");
		var data1 = {
			labels: dd_af,
			datasets: [
			{
				label: "营业额",
				backgroundColor: "rgba(60,184,120,0.4)",
				borderColor: "rgba(60,184,120,0.4)",
				pointBorderColor: "rgb(60,184,120)",
				pointHighlightStroke: "rgba(60,184,120,1)",
				data: income_list
			}
		]
		};
		var areaChart = new Chart(ctx1, {
			type:"line",
			data:data1,
			options: {
				tooltips: {
					mode:"label",
                    backgroundColor:'rgba(47,44,44,.9)',
					cornerRadius:0,
					footerFontFamily:"'Varela Round'"
				},
				elements:{
					point: {
						hitRadius:90
					}
				},

				scales: {
					yAxes: [{
						stacked: true,
						gridLines: {
							color: "#eee",
						},
						ticks: {
							fontFamily: "Varela Round",
							fontColor:"#2f2c2c"
						}
					}],
					xAxes: [{
						stacked: true,
						gridLines: {
							color: "#eee",
						},
						ticks: {
							fontFamily: "Varela Round",
							fontColor:"#2f2c2c"
						}
					}]
				},
				animation: {
					duration:	3000
				},
				responsive: true,
				maintainAspectRatio:false,
				legend: {
					display: false
				}
			}
		});
	}
});

function get_xaxis_date(date_list){
    /**
	 * right_date			时间右区间20170803
	 * get_type				获取类型1-day, 2-month, 3-year
     */
    var date_list_re = [];
    for(var i=0;i<date_list.length;i++){
    	var date_str = date_list[i].toString();
    	if(date_str.length===8){
    		var temp_str = date_str[4]+date_str[5]+"-"+date_str[6]+date_str[7];
    		date_list_re.push(temp_str);
		}
		else if(date_str.length===6){
    		date_list_re = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"];
		}
		else{
			date_list_re.push(date_str)
		}
	}
	return date_list_re
}
/*****Ready function end*****/