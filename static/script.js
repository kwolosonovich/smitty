document.addEventListener("DOMContentLoaded", function () {
  // get elements
  let like = document.getElementsByClassName("like");
  var likeImages = document.querySelectorAll(".like");

  like.addEventListener("click", addLike);

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

  // dismissal of an alert message
  $(".alert").alert();

  // render search results
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

  // like image event listener - change to solid
  // function add_like(x) {
  //   x.classList.toggle("fas fa-thumbs-up");
  // }

  //event listener for like
  like.addEventListener("click", function (e) {
    e.preventDefault();
    console.log(e);
    // change to solid
    like.classList.toggle("fas fa-thumbs-up");
  });

  function likeImage(like) {
    like.classList.toggle("fa-thumbs-down");
  }

  function addLike() {
    console.log("clicked");
  }
  likeImages.addEventListener("click", function (e) {
    e.preventDefault();
    console.log(e);
    like.classList.toggle("fas fa-thumbs-up");
  });

  function likeImages(like) {
    like.classList.toggle("fas fa-thumbs-up");
  }

  function likeImages() {
    console.log("clicked");
  }

  $('.like').on('click',function(e) {
    e.preventDefault();
    console.log('clicked')
  } )
});
