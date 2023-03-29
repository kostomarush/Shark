var chrt = document.getElementById("chartId").getContext("2d");
      var chartId = new Chart(chrt, {  type: 'doughnut',  data: {  labels: ["Open", "Filter", "Close"],  
      datasets: [{  label: "online tutorial subjects",  data: [20, 40, 13],  
      backgroundColor: ['#33ce7a', '#ffc107', '#dc3545'],  
      hoverOffset: 3}],
         },  options: {  responsive: true,
         },
      });