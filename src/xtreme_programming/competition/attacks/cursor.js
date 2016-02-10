clearInterval(window.cursorInterval);
window.cursorInterval = setInterval(function() {
  if ($("body").css("cursor") == "none") {
    $("body").css("cursor", "default");
  } else {
    $("body").css("cursor", "none");
  }
}, 3000);
