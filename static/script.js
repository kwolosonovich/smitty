"use strict";

document.addEventListener("DOMContentLoaded", function () {

  // popovers Initialization
  $(function () {
    $('[data-toggle="popover"]').popover();
  });

  // carousel
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

  // dismissal of alert message
  $(function () {
    var selectedClass = "";
    $(".filter").click(function () {
      selectedClass = $(this).attr("data-rel");
      $("#gallery").fadeTo(100, 0.1);
      $("#gallery div")
        .not("." + selectedClass)
        .fadeOut()
        .removeClass("animation");
      setTimeout(function () {
        $("." + selectedClass)
          .fadeIn()
          .addClass("animation");
        $("#gallery").fadeTo(300, 1);
      }, 300);
    });
  });

  $(function () {
    $("#mdb-lightbox-ui").load("mdb-addons/mdb-lightbox-ui.html");
  });

});
