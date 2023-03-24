
function growthcompany(){
    setTimeout(()=>{
        var options1 = {
            series: [
                {
                    name: 'Airtel Money',
                    data: [680000, 830000, 600000, 720000, 750000, 918000, 600000, 580000, 880000, 560000, 787000, 699000]
                },
                {
                    name: "Moov Money",
                    data: [450000, 300000, 650000, 700000, 620000, 712000, 580000, 665000, 500000, 530000, 600000, 780000]
                },
            ],
        chart: {
            height: 330,
            type: 'line',
            zoom: {
            enabled: false
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
        dataLabels: {
            enabled: false
        },
        stroke: {
            width: [3, 3],
            curve:'smooth',
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
            categories: ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aout', 'Sept',
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
        document.getElementById('growthcompany').innerHTML = ''; 
        var chart1 = new ApexCharts(document.querySelector("#growthcompany"), options1);
        chart1.render();
    }, 300);
    
    };

function chartcompany() {
	'use strict';
	var options = {
		series: [{
		data: [500, 700, 418, 570, 640, 780, 990, 1100, 1200, 1380, 840, 580, 690,1380, 840, ]
	  }],
		chart: {
		type: 'bar',
		height: 300,
        toolbar: {
            show: false,
        },
	  },
	  plotOptions: {
		bar: {
		  borderRadius: 1,
		  horizontal: false,
          colwidth:'20%'
		}
	  },
	  colors:[myVarVal],
	  dataLabels: {
		enabled: false
	  },
	  xaxis: {
		labels: {
			show: false,
		},
		categories: [ '1', '2', '3','4','5','6','7','8','9','10','11','12','13','14','15'
		],
		axisBorder: {
			show: true,
			color: 'rgba(119, 119, 142, 0.05)',
		},
	  },
	  grid: {
		  borderColor: 'rgba(119, 119, 142, 0.1)',
	  }
	  };
      document.getElementById('chart-company').innerHTML = ''; 
	  var chart = new ApexCharts(document.querySelector("#chart-company"), options);
	  chart.render();
  
};


if ($('.chart-circle').length) {
		$('.chart-circle').each(function() {
			let $this = $(this);
			$this.circleProgress({
				fill: {
					color: $this.attr('data-color')
				},
				size: $this.height(),
				startAngle: -Math.PI / 4 * 2,
				emptyFill: '#f6f6f6',
				lineCap: 'round'
			});
		});
	}

        