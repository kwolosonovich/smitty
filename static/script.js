$(document).ready(function () {
  
  $(".carousel.carousel-multi-item.v-2 .carousel-item").each(function () {
    var next = $(this).next();
    if (!next.length) {
      next = $(this).siblings(":first");
    }
    next.children(":first-child").clone().appendTo($(this));

    for (var i = 0; i < 4; i++) {
      next = next.next();
      if (!next.length) {
        next = $(this).siblings(":first");
      }
      next.children(":first-child").clone().appendTo($(this));
    }
  });

  // SideNav Button Initialization
  // $(".button-collapse").sideNav2()
  // // SideNav Scrollbar Initialization
  // var sideNavScrollbar = document.querySelector(".custom-scrollbar");
  // var ps = new PerfectScrollbar(sideNavScrollbar);

  // (function () {
  //   "use strict";

  //   feather.replace();

  //   // Graphs
  //   var ctx = document.getElementById("myChart");
  //   // eslint-disable-next-line no-unused-vars
  //   var myChart = new Chart(ctx, {
  //     type: "line",
  //     data: {
  //       labels: [
  //         "Sunday",
  //         "Monday",
  //         "Tuesday",
  //         "Wednesday",
  //         "Thursday",
  //         "Friday",
  //         "Saturday",
  //       ],
  //       datasets: [
  //         {
  //           data: [15339, 21345, 18483, 24003, 23489, 24092, 12034],
  //           lineTension: 0,
  //           backgroundColor: "transparent",
  //           borderColor: "#007bff",
  //           borderWidth: 4,
  //           pointBackgroundColor: "#007bff",
  //         },
  //       ],
  //     },
  //     options: {
  //       scales: {
  //         yAxes: [
  //           {
  //             ticks: {
  //               beginAtZero: false,
  //             },
  //           },
  //         ],
  //       },
  //       legend: {
  //         display: false,
  //       },
  //     },
  //   });
  // })();


});
