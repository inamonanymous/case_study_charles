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
    series: [],
    chart: {
      height: 350,
      type: 'line',
      stacked: false,
    },
    stroke: {
      width: [0, 2, 5],
      curve: 'smooth'
    },
    
    fill: {
      opacity: [0.85, 0.25, 1],
      gradient: {
        inverseColors: false,
        shade: 'light',
        type: 'vertical',
        opacityFrom: 0.85,
        opacityTo: 0.55,
        stops: [0, 100, 100, 100]
      },
    },
    labels: [], // Populate with dynamic data
    markers: {
      size: 0,
    },
    xaxis: {
      type: 'dateyear',
    },
    yaxis: {
      title: {
        text: 'Trade',
        style: {
          color: '#3c3c40',
        },
      },
      min: 0,
    },
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function (y) {
          if (typeof y !== 'undefined') {
            return y.toFixed(0) + ' Trade';
          }
          return y;
        },
      },
    },
  };
  
  var areaChart = new ApexCharts(document.querySelector('#area-chart'), areaChartoptions);
  
  axios.get('/api/area_chart_data')
    .then(function (response) {
      console.log('Response from server:', response.data);
  
      // Access the data from the API response
      var data = response.data;
  
      // Update the labels with the years from your data
      areaChart.updateOptions({
        labels: data.years,
      });
  
      const productNames = Object.keys(data.data);
      // Create the series data for the area chart
      var seriesData = productNames.map(product => ({
        name: product,
        type: 'column',  // You can customize the type based on your requirements
        data: data.data[product]
      
      }));
      console.log(seriesData);

      // Update the series data
      areaChart.updateSeries(seriesData);
    })
    .catch(function (error) {
      console.error('Error fetching area chart data:', error);
    });
  areaChart.render();

  // RADAR AREA


// Initialize the radar chart


// Render the radar chart
