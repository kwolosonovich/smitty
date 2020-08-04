"use strict";

document.addEventListener("DOMContentLoaded", function () {
  // variables
  const BASE_URL = "http://127.0.0.1:5000/api";
  let likes = document.getElementsByClassName("far fa-thumbs-up like");

  
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


  // ********likes**********

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
    let url = elmts.children[5].getAttribute("value");
    let title = elmts.children[1].getAttribute("value");
    let artist = elmts.children[2].getAttribute('value');
    let date = elmts.children[3].getAttribute("value");
    let collection = elmts.children[4].getAttribute("value");
    let userId = elmts.children[6].getAttribute("value")

    let newImage = new Image(url, title, artist, date, collection)

    addFavorite(newImage, userId)
  }


  async function addFavorite(newImage, userId) {

    const response = await axios.post(`${BASE_URL}/${userId}/like`, newImage)
        
    if (response === 201) {
      console.log('added')
    }

  }

  function removeFav(elmts) {
    let userId = elmts.children[6].getAttribute("value");
    let url = elmts.children[5].getAttribute("value");
  
    let imageToUnlike = {
      'url': url
    }
      unlike(imageToUnlike, userId);
  }

  async function unlike(imageToUnlike, userId) {
    const response = await axios.post(
      `${BASE_URL}/${userId}/unlike`,
      imageToUnlike
    );

    if (response === 201) {
      console.log("removed");
    }
  }

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

      let parentTag = this.parentElement;
      let elmts = parentTag.parentElement;
      favImage(elmts);
    } else {
      this.classList.remove("fas");
      this.classList.remove("fa-thumbs-up");
      this.classList.remove("like");
      this.classList.add("far");
      this.classList.add("fa-thumbs-up");
      this.classList.add("like");

      let parentTag = this.parentElement;
      let elmts = parentTag.parentElement;
      removeFav(elmts)
    }
  }
  // add event listener to like icon
  for (var i = 0; i < likes.length; i++) {
    likes[i].addEventListener("click", toggleLike, false);
  }

  // ********render likes***********

  let userLikes = document.getElementById("likes").addEventListener("click", getUserId);
  
  function getUserId(e) {
    e.preventDefault();

    let parentTag = this.parentElement;
    let userId = parentTag.getAttribute('value')

    getLikes(userId)
  }

  async function getLikes(userId) {
    const response = await axios.get(`${BASE_URL}/${userId}/likes`);

      console.log(response.data);
            console.log('status')

      renderLikes(response);
  }
  

  async function renderLikes(response) {

    console.log('response');
    console.log(response);
    console.log("response.data");
    console.log(response.data)
    console.log('response.data[0]');
    console.log(response.data[0]);
    console.log(response.data[0].artist)
  }

});
