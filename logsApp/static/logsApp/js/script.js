function hideErrorMessage(elementId) {
  setTimeout(function () {
    var message = document.getElementById(elementId);
    if (message) {
      message.style.transition = "opacity 1s ease-out";
      message.style.opacity = 0;
      setTimeout(function () {
        message.style.display = "none";
      }, 1000);
    }
  }, 5000);
}

console.log("working");
