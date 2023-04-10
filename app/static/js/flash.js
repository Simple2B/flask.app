const flashIconToClose = document.querySelector(".close");
const flashContainer = document.querySelector(".close-js");
if (flashIconToClose) {
  flashIconToClose.addEventListener("click", () => {
    flashContainer.classList.add("hidden");
  });  
}
