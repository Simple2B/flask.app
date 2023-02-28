const flashIconToClose = document.querySelector(".close");
const flashContainer = document.querySelector(".close-js");
flashIconToClose.addEventListener("click", () => {
  flashContainer.classList.add("hidden");
});
