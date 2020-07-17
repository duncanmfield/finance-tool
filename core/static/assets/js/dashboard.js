(function($) {
  'use strict';
  $.fn.andSelf = function() {
    return this.addBack.apply(this, arguments);
  }

  $(function() {
    if ($("#account_values_chart").length) {
      var $accountValuesChart = $("#account_values_chart");
      $.ajax({
        url: $accountValuesChart.data("url"),
        success: function (data) {
          var ctx = $accountValuesChart[0].getContext("2d");
          var areaOptions = {
            responsive: true,
            maintainAspectRatio: true,
            segmentShowStroke: false,
            cutoutPercentage: 70,
            elements: {
              arc: {
                  borderWidth: 0
              }
            },
            legend: {
              display: false
            },
            tooltips: {
              enabled: true
            }
          }
          var accountChartPlugins = {
            beforeDraw: function(chart) {
              var width = chart.chart.width,
                  height = chart.chart.height,
                  ctx = chart.chart.ctx;

              ctx.restore();
              var fontSize = 1;
              ctx.font = fontSize + "rem Rubik";
              ctx.textAlign = 'left';
              ctx.textBaseline = "middle";
              ctx.fillStyle = "#ffffff";

              var text = data.centerText,
                  textX = Math.round((width - ctx.measureText(text).width) / 2),
                  textY = height / 2.2;

              ctx.fillText(text, textX, textY);

              ctx.restore();
              var fontSize = 0.75;
              ctx.font = fontSize + "rem Rubik";
              ctx.textAlign = 'left';
              ctx.textBaseline = "middle";
              ctx.fillStyle = "#6c7293";

              var subText = data.centerSubText,
                  subTextX = Math.round((width - ctx.measureText(subText).width) / 2),
                  subTextY = height / 1.7;

              ctx.fillText(subText, subTextX, subTextY);
              ctx.save();
            }
          }

          new Chart(ctx, {
            type: 'doughnut',
            options: areaOptions,
            plugins: accountChartPlugins,
            data: {
              labels: data.labels,
              datasets: [{
                data: data.data,
                backgroundColor: palette(data.colorPalette, data.data.length).map(function(hex) {
                    return '#' + hex;
                })
              }]
            }
          });
        }
      });
    }
  });
})(jQuery);