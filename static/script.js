"use strict";

document.addEventListener("DOMContentLoaded", function () {
  // variables
  const BASE_URL = "http://127.0.0.1:5000/api";
  let likes = document.getElementsByClassName("far fa-thumbs-up like");
  
  // // popovers Initialization
  // $(function () {
  //   $('[data-toggle="popover"]').popover();
  // });

  // carousel
  // $(".carousel.carousel-multi-item.v-2 .carousel-item").each(function () {
  //   var next = $(this).next();
  //   if (!next.length) {
  //     next = $(this).siblings(":first");
  //   }
  //   next.children(":first-child").clone().appendTo($(this));

  //   for (var i = 0; i < 4; i++) {
  //     next = next.next();
  //     if (!next.length) {
  //       next = $(this).siblings(":first");
  //     }
  //     next.children(":first-child").clone().appendTo($(this));
  //   }
  // });

  // dismissal of alert message
  // $(".alert").alert();

  // render search results
  // var selectedClass = "";

  // $(".filter").click(function () {
  //   selectedClass = $(this).attr("data-rel");
  //   $("#gallery").fadeTo(100, 0.1);
  //   $("#gallery div")
  //     .not("." + selectedClass)
  //     .fadeOut()
  //     .removeClass("animation");
  //   setTimeout(function () {
  //     $("." + selectedClass)
  //       .fadeIn()
  //       .addClass("animation");
  //     $("#gallery").fadeTo(300, 1);
  //   }, 300);
  // });


  // image class
  class Image {
    constructor(url, title, artist, date, collection) {
      this.url = url;
      this.title = title;
      this.artist = artist;
      this.date = date;
      this.collection = collection;
    }
  }

  function favImage(elmts) {
    // console.log(elmts.children)
    
  //   // console.log(elmts.childNodes[2].getAttribute["value"]);

  //   let url = elmts.childdren[2].getAttribute("value");
  //   let title = elmts.children[1].getAttribute("value");
  //   let artist = elmts.children[3].getAttribute("value");
  //   let date = elmts.children[4].getAttribute("value");
  //   let collection = elmts.children[4].getAttribute("value");
  //   let userId = elmts.children[6].getAttribute("value");

  //   console.log(title, artist, collection, userId)

  //   // let newImage = new Image(url, title, artist, date, collection)
  //   // console.log(newImage)
  //   // console.log(elem.children);
  //   // addFavorite(newImage, userId)
  }


  async function addFavorite(newImage, userId) {
    console.log(userId)
    const response = await axios.post(`${BASE_URL}/${userId}/like`)
    console.log('addFavorite')
  }


  // toggle image like icon
  function toggleLike(e) {
    e.preventDefault();
    console.log("toggleLike")
    var icon = this.className;
    console.log(icon)
    if (icon === "far fa-thumbs-up like") {
      console.log("if")
      this.classList.remove("far");
      this.classList.remove("fa-thumbs-up");
      this.classList.remove("like");
      this.classList.add("fas");
      this.classList.add("fa-thumbs-up");
      this.classList.add("like");

      // let parentTag = this.parentElement;
      // let elmts = parentTag.parentElement;
      favImage(elmts);
    } else {
      console.log("else")
      this.classList.remove("fas");
      this.classList.remove("fa-thumbs-up");
      this.classList.remove("like");
      this.classList.add("far");
      this.classList.add("fa-thumbs-up");
      this.classList.add("like");
    }
  }
  // add event listener to like icon
  for (var i = 0; i < likes.length; i++) {
    likes[i].addEventListener("click", toggleLike, false);
  }
});
