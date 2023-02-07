

//paexchart
function sales(){
setTimeout(()=>{
	var options1 = {
		series: [
			{
				name: 'Amount Used',
				data: [40, 35, 78, 50, 75, 48, 62, 47, 80, 56, 40, 50]
			},
			{
				name: "Total Budget",
				data: [45, 30, 65, 35, 50, 70, 38, 60, 36, 65, 32, 45]
			},
		],
	chart: {
		height: 330,
		type: 'bar',
        stacked: true,
		zoom: {
		enabled: false,
		},
		toolbar: {
			show: false,
		},
		dropShadow: {
			enabled: false,
			enabledOnSeries: undefined,
			top: 5,
			left: 0,
			blur: 0,
			color: '#000',
			opacity: 0,
		},
	},
    plotOptions: {
      bar: {
        borderRadius: 1,
        horizontal: false,
        columnWidth: '30%',
      }
    },
	dataLabels: {
		enabled: false
	},
	stroke: {
		width: [1, 1],
		dashArray: [0, 0],
	},
	legend: {
		show: true,
		position: 'top',
		horizontalAlign: 'center',
		fontWeight: 600,
		tooltipHoverFormatter: function(val, opts) {
		return val + ' - ' + opts.w.globals.series[opts.seriesIndex][opts.dataPointIndex] + ''
		},
		labels: {
			colors: '#74767c',
		},
		markers: {
			width: 9,
			height: 9,
			strokeWidth: 0,
			radius: 12,
			offsetX: 0,
			offsetY: 0
		},
	},
	markers: {
		size: [0, 0],
		hover: {
		sizeOffset: 4
		}
	},
	colors: [myVarVal, '#fb8d34'],
	xaxis: {
		categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
		'Oct', 'Nov', 'Dec'
		],
		axisBorder: {
			show: true,
			color: 'rgba(119, 119, 142, 0.05)',
		},
		axisTicks: {
			show: true,
			color: 'rgba(119, 119, 142, 0.05)',
		},
	},
	tooltip: {
		y: [
		{
			title: {
			formatter: function (val) {
				return val + " (mins)"
			}
			}
		},
		{
			title: {
			formatter: function (val) {
				return val + " per session"
			}
			}
		},
		{
			title: {
			formatter: function (val) {
				return val;
			}
			}
		}
		]
	},
	grid: {
		borderColor: 'rgba(119, 119, 142, 0.1)',
	}
	};
	document.getElementById('sales-budaget').innerHTML = ''; 
	var chart1 = new ApexCharts(document.querySelector("#sales-budaget"), options1);
	chart1.render();
}, 300);

}


function chartpai(){
	var options = {
		series: [70],
		chart: {
		height: 250,
		type: 'radialBar',
	},
	plotOptions: {
		radialBar: {
		hollow: {
			size: '70%',
		}
		},
	},
	colors:[myVarVal],
	labels: ['Sales'],
	};
	document.getElementById('chart-pai').innerHTML = '';
	var chart = new ApexCharts(document.querySelector("#chart-pai"), options);
	chart.render();

}
