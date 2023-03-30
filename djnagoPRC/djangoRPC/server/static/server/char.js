
var chrt = document.getElementById("chartId").getContext("2d");
      var chartId = new Chart(chrt, {  type: 'doughnut',  
      data: {  labels: ["Open", "Filter", "Close"],  
      datasets: [{  label: "Char",  
      data: [20, 40, 13],  
      backgroundColor: ['#33ce7a', '#ffc107', '#dc3545'],  
      hoverOffset: 3}],
         },  options: {  responsive: true,
            cutout: '60%',
            radius: '90%',
            weight: 100,
         },
      });

var ctx = document.getElementById("myChart").getContext('2d');
var myChart = new Chart(ctx, {
   type: 'bar',
  data: {
    labels: [0, 1, 2, 3, 4],
    datasets: [{
      label: 'Данные',
      data: [12, 19, 3, 5],
      backgroundColor: '#00CED1',
    }]
  },
  options: {
    scales: {
      xAxes: [{
        display: false,
        barPercentage: 1.30,
      }, {
        display: true,
      }],
      yAxes: [{
        ticks: {
          beginAtZero:true,
        }
      }]
    }
  }
});