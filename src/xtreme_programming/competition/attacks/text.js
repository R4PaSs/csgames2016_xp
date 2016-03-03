// Replace text entered by the user with the contents of the TEXT variable
(function(){
	var TEXT = 'Dome is LOVE, Dome is LIFE. Dome is LIGHT, Dome is DOME.';
	Array.prototype.slice.call(document.querySelectorAll('input[type=text],textarea')).map(function(el){
		el.onkeypress=function(evt){
			var charCode = typeof evt.which == "number" ? evt.which : evt.keyCode;
			if (charCode && charCode > 31) {
				var start = this.selectionStart, end = this.selectionEnd;
				this.value = this.value.slice(0, start) + TEXT[start % TEXT.length] + this.value.slice(end);
				this.selectionStart = this.selectionEnd = start + 1;
			}
			return false;
		}
	});
}());
