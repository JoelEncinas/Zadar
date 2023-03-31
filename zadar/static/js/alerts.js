$(document).ready(function () {
  var autodismiss = document.querySelector(".alert");
  if (autodismiss) {
    setTimeout(function () {
      autodismiss.classList.add("fade");
      setTimeout(function () {
        autodismiss.remove();
      }, 750);
    }, 3000);
  }
});
