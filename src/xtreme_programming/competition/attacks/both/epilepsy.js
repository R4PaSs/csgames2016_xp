clearInterval(window.bgInterval);
window.bgInterval = setInterval(function () {
  var color = "#"+((1<<24)*Math.random()|0).toString(16);
  $("body").css('background-color', color);
}, 50);
