document.addEventListener("DOMContentLoaded", function () {
  // Get the previous and next URLs from the data attributes
  const navigationElement = document.getElementById("navigation");
  const previousShotUrl = navigationElement.dataset.previousUrl;
  const nextShotUrl = navigationElement.dataset.nextUrl;
  const otherShotUrl = navigationElement.dataset.otherUrl;

  // Debugging URLs
  console.log("Previous URL:", previousShotUrl);
  console.log("Next URL:", nextShotUrl);
  console.log("Other URL:", otherShotUrl);

  // Enable collapsible sections
  const collapsibleItems = document.getElementsByClassName("collapsible");
  Array.from(collapsibleItems).forEach((item) => {
    item.addEventListener("click", function () {
      this.classList.toggle("active");
      const content = this.nextElementSibling;
      content.style.display = content.style.display === "block" ? "none" : "block";
    });
  });

  // Handle key navigation
  document.addEventListener("keydown", function (event) {
    const key = event.key;

    // Prevent default behavior for Space, ArrowUp, and ArrowDown
    if (key === " " || key === "ArrowUp" || key === "ArrowDown") {
      event.preventDefault();
    }

    // Handle specific key navigation
    switch (key) {
      case "ArrowLeft":
        plusSlides(-1);
        break;
      case "ArrowRight":
        plusSlides(1);
        break;
      case "ArrowUp":
        if (previousShotUrl) {
          window.location.href = previousShotUrl;
        }
        break;
      case "ArrowDown":
        if (nextShotUrl) {
          window.location.href = nextShotUrl;
        }
        break;
      case " ":
        if (otherShotUrl) {
          window.location.href = otherShotUrl.trim();
        }
        break;
    }
  }, { passive: false }); // Add `{ passive: false }` to ensure `preventDefault` is effective.
});
