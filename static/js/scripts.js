// SIDEBAR TOGGLE

document.addEventListener("DOMContentLoaded", function () {
  // SIDEBAR TOGGLE

  var sidebarOpen = false;
  var sidebar = document.getElementById('sidebar');

  function openSidebar() {
      if (!sidebarOpen) {
          sidebar.classList.add('sidebar-responsive');
          sidebarOpen = true;
      }
  }

  function closeSidebar() {
      if (sidebarOpen) {
          sidebar.classList.remove('sidebar-responsive');
          sidebarOpen = false;
      }
  }

  // BAR CHART

  var barChartoptions = {
    chart: {
      type: 'bar',
      height: 350,
      toolbar: {
        show: false,
      },
    },
    colors: [
      '#2e7d32',
      '#2962ff',
      '#d50000',
      '#565b6e',
    ],
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '55%',
        endingShade: 'rounded',
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      show: true,
      width: 2,
      colors: ['transparent'],
    },
    xaxis: {},  // Remove 'categories' property here
    yaxis: {
      title: {
        text: 'FARMERS TRADE',
        style: {
          color: "#3c3c40",
        },
      },
      labels: {
        style: {
          colors: "#3c3c40",
        },
      },
    },
    fill: {
      opacity: 1,
    },
    grid: {
      borderColor: "#55596e",
      yaxis: {
        lines: {
          show: true,
        },
      },
      xaxis: {
        lines: {
          show: true,
        },
      },
    },
    legend: {
      lines: {
        colors: "bottom",
      },
      tooltip: {
        y: {
          formatter: function (val) {
            return 'FARMER' + 'TRADE';
          },
        },
      },
    },
    series: [], // Initially empty
  };
  
  var chart = new ApexCharts(document.querySelector("#bar-chart"), barChartoptions);
  
  // Fetch data from Flask and update the chart series
  axios.get('/api/bar_chart_data')
  .then(function (response) {
    console.log('Response from server:', response.data);

    // Access x-axis categories from the API response
    var xaxisCategories = response.data.xaxis.categories;
    console.log('X-Axis Categories:', xaxisCategories);
    
    // Assuming your API response is an object with keys 'Rice', 'Sugar', 'Oil', 'Vegetable'
    // Create an array of objects from the response to match the expected series format
    var seriesData = Object.keys(response.data.data).map(function(key) {
      return {
        name: key,
        data: response.data.data[key]
      };
    });

    // Update the series data with the newly created array
    chart.updateSeries(seriesData);

    // Now, x-axis categories are populated with the values from the API response
    chart.updateOptions({
      xaxis: {
        categories: xaxisCategories
      }
    });
  })
  .catch(function (error) {
    console.error('Error fetching bar chart data:', error);
  });
  
  chart.render();

  // AREA CHART

  var areaChartoptions = {
    series: [{
    name: 'Rice',
    type: 'column',
    data: [54, 51, 30, 97, 43, 72, 67, 71, 54, 42, 50]
  }, {
    name: 'Sugar',
    type: 'area',
    data: [44, 55, 41, 67, 22, 43, 21, 41, 56, 27, 43]
  }, {
    name: 'Oil',
    type: 'line',
    data: [30, 25, 36, 30, 45, 35, 64, 52, 59, 36, 39]
  }, {
    name: 'Vagetable',
    type: 'column',
    data: [35, 55, 76, 39, 85, 55, 64, 72, 69, 26, 59]
 }],
    chart: {
    height: 350,
    type: 'line',
    stacked: false,
  },
  stroke: {
    width: [0, 2, 5],
    curve: 'smooth'
  },
  plotOptions: {
    bar: {
      columnWidth: '50%'
    }
  },
  
  fill: {
    opacity: [0.85, 0.25, 1],
    gradient: {
      inverseColors: false,
      shade: 'light',
      type: "vertical",
      opacityFrom: 0.85,
      opacityTo: 0.55,
      stops: [0, 100, 100, 100]
    }
  },
  labels: ['2018', '2018', '2019', '2019', '2020', '2020', '2021',
    '2021', '2022', '2023', '2023'],
  markers: {
    size: 0
},
  xaxis: {
    type: 'dateyear',
  },
  yaxis: {
    title: {
      text: 'Trade',
      style: {
        color: "#3c3c40",
    },
    },
    min: 0
  },
  tooltip: {
    shared: true,
    intersect: false,
    y: {
      formatter: function (y) {
        if (typeof y !== "undefined") {
          return y.toFixed(0) + " Trade";
        }
        return y;
  
      }
    }
  }
  };

  var areaChart = new ApexCharts(document.querySelector("#area-chart"), areaChartoptions);
  areaChart.render();

  // RADAR AREA

  var radarChartoptions = {
    series: [{
    name: 'Series 1',
    data: [80, 50, 30, 40, 100, 20],
  }, {
    name: 'Series 2',
    data: [20, 30, 40, 80, 20, 80],
  }, {
    name: 'Series 3',
    data: [44, 76, 78, 13, 43, 10],
  }],
    chart: {
    height: 350,
    type: 'radar',
    dropShadow: {
      enabled: true,
      blur: 1,
      left: 1,
      top: 1
    }
  },
  title: {
    text: 'Statistic of salers:',
    style: {
      colors: "#f5f7ff",
    },
  },
  stroke: {
    width: 2
  },
  fill: {
    opacity: 0.1
  },
  markers: {
    size: 0
  },
  xaxis: {
    categories: ['2018', '2019', '2020', '2021', '2022', '2023']
  }
  };

  var radarChart = new ApexCharts(document.querySelector("#radar-chart"), radarChartoptions);
  radarChart.render();
});