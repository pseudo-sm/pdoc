function checkScroll() {
  var startY = $('.navbar').height() * 2; //The point where the navbar changes in px

  if ($(window).scrollTop() > startY) {
    if(!(document.querySelector(".navbar").classList.contains("def-scrl"))){
      $('.navbar').addClass("scrld");
      $('.navbar').removeClass("unscrld");
    }
    $('.back-to-top').show(1000);
  } else {
    if(!(document.querySelector(".navbar").classList.contains("def-scrl"))){
      $('.navbar').addClass("unscrld");
      $('.navbar').removeClass("scrld");
    }
    $('.back-to-top').hide(1000);
  }
}
var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    $('.navbar').slideDown(200);
  } else {
    $('.navbar').slideUp(200);
  }
  prevScrollpos = currentScrollPos;
};


if ($('.navbar').length > 0) {
  $(window).on("scroll load resize", function () {
    checkScroll();
  });
}
$(document).ready(function () {
  $('.navbar-light .dmenu').hover(function () {
    $(this).find('.sm-menu').first().stop(true, true).slideDown(150);
  }, function () {
    $(this).find('.sm-menu').first().stop(true, true).slideUp(105)
  });
});
$('.testi1').owlCarousel({
  loop: true,
  margin: 30,
  nav: false,
  dots: true,
  autoplay: true,
  responsiveClass: true,
  responsive: {
    0: {
      items: 1,
      nav: false
    },
    1024: {
      items: 2
    }
  }
});

function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}
AOS.init({
  disable: 'mobile'
});

function statsHide() {
  $("#mySidenav").hide();
}; 
document.onreadystatechange = function() { 
  if (document.readyState !== "complete") { 
      document.querySelector("body").style.visibility = "hidden"; 
      document.querySelector("#loader").style.visibility = "visible"; 
  } else { 
      document.querySelector("#loader").style.display = "none"; 
      document.querySelector("body").style.visibility = "visible"; 
  } 
};
function remove_alert() {
  alert = document.getElementsByClassName("alert")[0];
  alert.remove();
}