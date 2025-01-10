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

function toggleDateInput() {
  var dateType = document.getElementById("dateType").value;
  document.getElementById("dayInput").style.display =
    dateType === "day" ? "block" : "none";
  document.getElementById("monthInput").style.display =
    dateType === "month" ? "block" : "none";
  document.getElementById("yearInput").style.display =
    dateType === "year" ? "block" : "none";
}

function toggleFilters() {
  var filtersMain = document.getElementById("filtersMain");
  if (filtersMain.classList.contains("show")) {
    filtersMain.classList.remove("show");
    setTimeout(function () {
      filtersMain.style.display = "none";
    }, 500); // Match the transition duration
  } else {
    filtersMain.style.display = "block";
    setTimeout(function () {
      filtersMain.classList.add("show");
    }, 10); // Slight delay to trigger the transition
  }
}

document.addEventListener("DOMContentLoaded", function () {
  var tableContainer = document.getElementById("tableContainer");
  tableContainer.addEventListener("scroll", function () {
    if (tableContainer.scrollTop === 0) {
      window.scrollBy(0, -1);
    } else if (
      tableContainer.scrollTop + tableContainer.clientHeight >=
      tableContainer.scrollHeight
    ) {
      window.scrollBy(0, 1);
    }
  });
});

// forms show hide button
function toggleFineForm() {
  var form = document.getElementById("fineForm");
  if (form.style.display === "none" || form.style.opacity === "0") {
    form.style.display = "block";
    setTimeout(function () {
      form.style.opacity = "1";
    }, 10);
  } else {
    form.style.opacity = "0";
    setTimeout(function () {
      form.style.display = "none";
    }, 500);
  }
}

function toggleAccidentForm() {
  var form = document.getElementById("addEventForm");
  if (form.style.display === "none" || form.style.opacity === "0") {
    form.style.display = "block";
    setTimeout(function () {
      form.style.opacity = "1";
    }, 10);
  } else {
    form.style.opacity = "0";
    setTimeout(function () {
      form.style.display = "none";
    }, 500);
  }
}
