document.addEventListener("DOMContentLoaded", function () {
  let slidePosition = 1;
  SlideShow(slidePosition);

  // Forward/backward controls
  function plusSlides(n) {
    SlideShow(slidePosition += n);
  }

  // Thumbnail image controls
  function currentSlide(n) {
    SlideShow(slidePosition = n);
  }

  function SlideShow(n) {
    const slides = document.getElementsByClassName("Containers");
    const dots = document.getElementsByClassName("dots");

    if (n > slides.length) slidePosition = 1;
    if (n < 1) slidePosition = slides.length;

    // Hide all slides
    for (let i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
    }

    // Remove "enable" class from all dots
    for (let i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" enable", "");
    }

    // Show the current slide and activate the corresponding dot
    if (slides[slidePosition - 1]) {
      slides[slidePosition - 1].style.display = "block";
    }
    if (dots[slidePosition - 1]) {
      dots[slidePosition - 1].className += " enable";
    }
  }

  // Expose plusSlides and currentSlide globally if needed
  window.plusSlides = plusSlides;
  window.currentSlide = currentSlide;
});
