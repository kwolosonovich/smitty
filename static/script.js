document.addEventListener("DOMContentLoaded", function () {
  // get elements
  let likes = document.getElementsByClassName("far fa-thumbs-up like");
  // var like = document.querySelectorAll(".like");
  console.log(likes)
  // like.addEventListener("click", addLike);

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

  // for(i=0; i < like.length; i++) {
  //   like[i].addEventListener("click", function (e) {
  //     e.preventDefault();
  //     console.log(e);
  //     // change to solid
  //     console.log(like[i])
  //     like[i].toggle("fas fa-thumbs-up liked");

  //   });

  // }

  // like.forEach(function (element) {
  //   element.addEventListener("click", function(e){
  //     e.preventDefault();
  //     console.log(e);
  //     // change to solid
  //     // console.log(like[i])
  //     element.toggle("fas fa-thumbs-up liked");
  //   })
  // })
  function toggleLike() {
    var icon = this.className
    // console.log(icon)
    if (icon === "far fa-thumbs-up like"){
      // console.log("if")
      this.classList.remove("far")      
      this.classList.remove("fa-thumbs-up")
      this.classList.remove("like")
      this.classList.add("fas");
      this.classList.add("fa-thumbs-up")
      this.classList.add("like")

    } else {
      // console.log("else")
      this.classList.remove("fas")
      this.classList.remove("fa-thumbs-up")
      this.classList.remove("like")
      this.classList.add("far")
      this.classList.add("fa-thumbs-up")
      this.classList.add("like")

    }
  }
  for (var i=0; i < likes.length; i++) {
    likes[i].addEventListener('click', toggleLike, false)
  }

});
