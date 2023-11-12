function toggleSidebar() {
  var sidebar = document.getElementById('sidebar');
  sidebar.classList.toggle('sidebar-responsive');
}

// If sidebar-responsive is the class that shows the sidebar, this function will work.
// Ensure that the sidebar has the correct styles for the sidebar-responsive class in your CSS.

document.addEventListener("DOMContentLoaded", function () {
  // Attach the toggle function to the menu icon and close icon
  document.querySelector('.menu-icon').addEventListener('click', toggleSidebar);
  document.querySelector('.sidebar-title .material-symbols-outlined').addEventListener('click', toggleSidebar);

  // Add functionality for sidebar list items to toggle content
  var sidebarListItems = document.querySelectorAll('.sidebar-list-item');
  sidebarListItems.forEach(function (item) {
    item.addEventListener('click', function () {
      // Assuming that you have the data-target attribute set correctly on your list items
      var contentId = item.getAttribute('data-target');
      var contentDivs = document.querySelectorAll('.content-div');

      contentDivs.forEach(function (div) {
        div.style.display = div.id === contentId ? 'block' : 'none';
      });
    });
  });

  

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
  
      // Create the series data for the area chart
      var seriesData = [
        { name: 'Rice', type: 'column', data: data.data.Rice },
        { name: 'Sugar', type: 'area', data: data.data.Sugar },
        { name: 'Oil', type: 'line', data: data.data.Oil },
        { name: 'Vegetable', type: 'column', data: data.data.Vegetable },
      ];
      console.log(seriesData);

      // Update the series data
      areaChart.updateSeries(seriesData);
    })
    .catch(function (error) {
      console.error('Error fetching area chart data:', error);
    });
  
  areaChart.render();
















   
  // RADAR AREA

  var radarChartoptions = {
    series: [{
     
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
  
  };
  var radarChart = new ApexCharts(document.querySelector("#radar-chart"), radarChartoptions);
  axios.get('/api/radar_chart_data')
  .then(function (response) {
    var radarData = response.data;
    var seriesData = [];

    console.log("Radar Chart Response Data:", radarData); // Debugging

    Object.keys(radarData).forEach(function(seriesName) {
      if (Array.isArray(radarData[seriesName])) {
        seriesData.push({
          name: seriesName,
          data: radarData[seriesName]
        });
      }
    });

    console.log("Radar Chart Series Data:", seriesData); // Debugging

    radarChart.updateOptions({
      series: seriesData
    });
  })
  .catch(function(error) {
    console.error('Error fetching radar chart data:', error);
  });

radarChart.render();
});