clearInterval(window.zoomInterval);
window.zoomInterval = setInterval(function(){
  var rand = Math.random();
  var _currentZoom = window.currentZoom;

  var newZoom;
  if (rand > 0.5) {
   newZoom = _currentZoom + Math.random() / 2;
  } else {
    newZoom = _currentZoom - Math.random() / 2;
  }

  if (newZoom > 2.5) {
    newZoom = 2.5;
  } else if (newZoom < 0.5) {
    newZoom = 0.5;
  }

  window.currentZoom = newZoom;

  ['', '-ms-', '-webkit-', '-o-', '-moz-'].map(function(prefix){
		document.body.style[prefix + 'transition'] = prefix + 'transform .7s';
		document.body.style[prefix + 'transform'] = 'scale('+ newZoom.toString() + ', ' + newZoom.toString() +')';
	});

}, 800);
