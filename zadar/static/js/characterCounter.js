$(document).ready(function () {
  $("#body").on("input", function () {
    var maxlength = $(this).attr("maxlength");
    var currentLength = $(this).val().length;
    $("#character-counter").text(currentLength + "/ " + maxlength);
  }).trigger("input");
});
