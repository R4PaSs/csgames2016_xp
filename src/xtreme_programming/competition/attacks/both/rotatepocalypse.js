setTimeout(function(){
    document.onmousemove = document.onkeypress = function(){
        ['', '-ms-', '-webkit-', '-o-', '-moz-'].map(function(prefix){
            document.body.style[prefix + 'transition'] = prefix + 'transform 10s';
            document.body.style[prefix + 'transform'] = 'rotate(360deg)';
        });
    }
    setTimeout(function () {
        document.onmousemove = document.onkeypress = function(){
            ['', '-ms-', '-webkit-', '-o-', '-moz-'].map(function(prefix){
                document.body.style[prefix + 'transition'] = prefix + 'transform 10s';
                document.body.style[prefix + 'transform'] = 'rotate(0deg)';
            });
        }
    }, 1000)
}, 1000);
