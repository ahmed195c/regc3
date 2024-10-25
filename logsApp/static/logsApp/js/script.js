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

let filtersElement = document.getElementsByClassName("filtersDw")[0]; // Select the first element with the class
let filtersBtnel = document.getElementById("filtersBtn");

filtersBtnel.addEventListener("click", showFilters); // Pass the function reference

function showFilters() {
  if (filtersElement.style.display === "block") {
    filtersElement.style.display = "none"; // Hide if currently shown
  } else {
    filtersElement.style.display = "block"; // Show if currently hidden
  }
}
