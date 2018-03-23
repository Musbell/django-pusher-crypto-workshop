var chart1;
var BITFINEX_COLOR = '#4995c4';
var BITSTAMP_COLOR = '#14A04B';

$(document).ready(() => {
  var dataChart1 = []
  var dataChart2 = [43934, 52503, 57177, 69658, 43934, 52503, 57177, 69658, 97031, 119931]
  var dataChart3 = [43934, 52503, 57177, 69658, 43934, 52503, 57177, 69658, 97031, 119931]

  Pusher.logToConsole = true;

  var btcPrices = []
  if ($('#chart-1').length) {
    chart1 = Highcharts.chart('chart-1', {
      chart: {
        type: 'spline'
      },
      title: {
        text: 'BTC Latest Prices'
      },
      xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: { // don't display the dummy year
            second: '%k:%M:%S',
            // month: '%k:%M',
            // year: '%b'
        },
        title: {
            text: 'Timestamp'
        },
        crosshair: true,
      },
      yAxis: {
        title: {
          text: 'Price'
        },
        labels: {
            align: 'left',
            x: -25,
            y: -1
        },
        opposite: true,
        showFirstLabel: false,
        tickPosition: 'inside'
      },
      legend: {
        enabled: false
      },
      credits: {
        enabled: false
      },
      plotOptions: {
          spline: {
              marker: {
                  enabled: true
              }
          }
      },
      tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '${point.y:.2f} @ {point.x:%k:%M:%S}'
      },
      series: [{
        name: 'Bitstamp',
        color: BITSTAMP_COLOR,
        data: []
      }, {
        name: 'Bitfinex',
        color: BITFINEX_COLOR,
        data: []
      }],
    });
  }

  if ($('#chart-2').length) {
    var chart2 = Highcharts.chart('chart-2', {
      chart: {
        type: 'spline'
      },
      title: {
        text: ''
      },
      xAxis: {
        categories: ['a', 'b', 'c', 'd', 'e', 'f'],
        crosshair: true,
      },
      yAxis: {
        title: {
          text: ''
        },
        labels: {
            align: 'left',
            x: -25,
            y: -1
        },
        opposite: true,
        showFirstLabel: false,
        tickPosition: 'inside'
      },
      legend: {
        enabled: false
      },
      credits: {
        enabled: false
      },
      plotOptions: {
          series: {
              label: {
                  connectorAllowed: false
              }
          }
      },
      series: [{
          name: 'Price',
          color: '#2ecc71',
          data: dataChart2
      }],
    });
  }

  if ($('#chart-3').length) {
    var chart3 = Highcharts.chart('chart-3', {
      chart: {
        type: 'spline'
      },
      title: {
        text: ''
      },
      xAxis: {
        categories: ['a', 'b', 'c', 'd', 'e', 'f'],
        crosshair: true,
      },
      yAxis: {
        title: {
          text: ''
        },
        labels: {
            align: 'left',
            x: -25,
            y: -1
        },
        opposite: true,
        showFirstLabel: false,
        tickPosition: 'inside'
      },
      legend: {
        enabled: false
      },
      credits: {
        enabled: false
      },
      plotOptions: {
          series: {
              label: {
                  connectorAllowed: false
              }
          }
      },
      series: [{
          name: 'Price',
          color: '#3498db',
          data: dataChart3
      }],
    });
  }
  //
  var pusher = new Pusher('6f4dce495b70f4f53d86', {
    encrypted: true
  });

  var channel = pusher.subscribe('prices__btc');
  channel.bind('price', function(data) {
    console.log(data)
    var series = 0;
    if (data.exchange === 'Bitfinex'){
      series = 1;
    }
    var price = [(new Date(data.timestamp)).getTime(), data.price]
    dataChart1.push(price)
    if(dataChart1.length >= 10){
      dataChart1 = dataChart1.slice(dataChart1.length - 10)
    }
    chart1.series[series].update({data: dataChart1})
  });
// // console.log(chart1.series[0].data)
// setInterval(function(){
//   var last = dataChart1[dataChart1.length - 1] || [Date.now(), 8581.32];
//   var n1 = Math.random() * 100
//   var n2 = Math.random() * 10
//   var symbol = 1;
//   if (n2 > 5){
//     symbol = -1
//   }
//   var new_point = [Date.now(), last[1] + (n1 * symbol)]
//
//
//   var data = dataChart1;
//   if(data.length >= 10){
//     data = dataChart1.slice(data.length - 10)
//   }
//
//   chart1.series[0].update({data: data})
//
//
//
//   // chart1.series[0].data.push([Date.UTC(2018, 3, 22, 20, 18, 22), 8581.32]);
//   // var data = [...chart1.series[0].data];
//   // chart1.series[0].addPoint([Date.UTC(2018, 3, 22, 20, 18, 22), 8581.32], true, true)
//   // chart1.series[0].addPoint(30, true, true)
//   // console.log()
//   // var data = [...chart1.series[0].data]
//   // var last = data[data.length - 1];
//   // var new_point = [Date.now(), last[1] + 10]
//   // data.push(new_point)
//   // console.log(data)
//   // // chart1.series[0].addPoint(new_point)
//   // chart1.series[0].update({data: data})
//   // data.push()
//   // chart1.series[0].setData(data)
//
//   // chart2.series[0].addPoint(599)
//   // chart1.series[0].addPoint([Date.UTC(2018, 3, 22, 21, 18, 22), 9000.32])
//   //
//   // chart1.series[0].update({data: data})
//
//   // dataChart1.shift()
// }, 2000);

  // console.log([...chart1.series[0].data])
  // FIXME: simulate Pusher event
  setInterval(function() {
    // update chart1
    // if (chart1) {
    //   var newPriceDataChart1 = 30000
    //   dataChart1.push(newPriceDataChart1)
    //   dataChart1.shift()
    //
    //   chart1.series[0].update({
    //     yData: dataChart1
    //   })
    //
    //   $('.price-btc').text(newPriceDataChart1)
    // }

    // update chart2
    if (chart2) {
      var newPriceDataChart2 = 100000
      dataChart2.push(newPriceDataChart2)
      dataChart2.shift()

      chart2.series[0].update({
        yData: dataChart2
      })

      $('.price-eth').text(newPriceDataChart2)
    }

    // update chart3
    if (chart3) {
      var newPriceDataChart3 = 150000
      dataChart3.push(newPriceDataChart3)
      dataChart3.shift()

      chart3.series[0].update({
        yData: dataChart3
      })

      $('.price-ltc').text(newPriceDataChart3)
    }
  }, 2500);
})
