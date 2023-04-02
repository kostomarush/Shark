var chrt = document.getElementById("chartId").getContext("2d");
var chartId = new Chart(chrt, {
  type: "doughnut",
  data: { labels: ["Open", "Filtered", "Closed", "Open|Filtered"], datasets: [{}] },
  options: { responsive: true, cutout: "60%", radius: "90%", weight: 100 },
});

var ctx = document.getElementById("myChart").getContext("2d");
var myChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: ["Клиент 1", "Клиент 2"],
    datasets: [
      {
        label: "Выполнено задач", 
      },
    ],
  },
});
