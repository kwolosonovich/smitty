"use strict";

document.addEventListener("DOMContentLoaded", function () {
  // variables
  const BASE_URL = "http://localhost:5000/api";
  // let likes = document.getElementsByClassName("far fa-thumbs-up like");

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

  // toggle image like icon
  function toggleLike(e) {
    e.preventDefault();
    var icon = this.className;
    if (icon === "far fa-thumbs-up like") {
      this.classList.remove("far");
      this.classList.remove("fa-thumbs-up");
      this.classList.remove("like");
      this.classList.add("fas");
      this.classList.add("fa-thumbs-up");
      this.classList.add("like");

    } else {
      this.classList.remove("fas");
      this.classList.remove("fa-thumbs-up");
      this.classList.remove("like");
      this.classList.add("far");
      this.classList.add("fa-thumbs-up");
      this.classList.add("like");
    }
  }
  // // add event listener to like icon
  for (var i = 0; i < likes.length; i++) {
    likes[i].addEventListener("click", toggleLike, false);
  }
});
