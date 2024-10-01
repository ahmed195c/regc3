console.log("working");

function fadeOutMessage(id) {
  var message = document.getElementById(id);
  if (message) {
    message.style.transition = "opacity 1s ease-out";
    message.style.opacity = 0;
    setTimeout(function () {
      message.style.display = "none";
    }, 1000);
  }
}